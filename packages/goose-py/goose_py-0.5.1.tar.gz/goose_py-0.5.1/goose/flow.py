import json
from contextlib import asynccontextmanager
from contextvars import ContextVar
from types import CodeType
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    NewType,
    Protocol,
    Self,
    overload,
)

from pydantic import BaseModel

from goose.agent import (
    Agent,
    AssistantMessage,
    GeminiModel,
    IAgentLogger,
    LLMMessage,
    SystemMessage,
    UserMessage,
)
from goose.errors import Honk
from goose.result import Result, TextResult
from goose.store import IFlowRunStore, InMemoryFlowRunStore

SerializedFlowRun = NewType("SerializedFlowRun", str)


class Conversation[R: Result](BaseModel):
    user_messages: list[UserMessage]
    result_messages: list[R]
    context: SystemMessage | None = None

    @property
    def awaiting_response(self) -> bool:
        return len(self.user_messages) == len(self.result_messages)

    def render(self) -> list[LLMMessage]:
        messages: list[LLMMessage] = []
        if self.context is not None:
            messages.append(self.context.render())

        for message_index in range(len(self.user_messages)):
            messages.append(
                AssistantMessage(
                    text=self.result_messages[message_index].model_dump_json()
                ).render()
            )
            messages.append(self.user_messages[message_index].render())

        if len(self.result_messages) > len(self.user_messages):
            messages.append(
                AssistantMessage(
                    text=self.result_messages[-1].model_dump_json()
                ).render()
            )

        return messages


class IAdapter[ResultT: Result](Protocol):
    __code__: CodeType

    async def __call__(
        self, *, conversation: Conversation[ResultT], agent: Agent
    ) -> ResultT: ...


class NodeState[ResultT: Result](BaseModel):
    task_name: str
    index: int
    conversation: Conversation[ResultT]
    last_hash: int

    @property
    def result(self) -> ResultT:
        if len(self.conversation.result_messages) == 0:
            raise Honk("Node awaiting response, has no result")

        return self.conversation.result_messages[-1]

    def set_context(self, *, context: SystemMessage) -> Self:
        self.conversation.context = context
        return self

    def add_result(
        self,
        *,
        result: ResultT,
        new_hash: int | None = None,
        overwrite: bool = False,
    ) -> Self:
        if overwrite and len(self.conversation.result_messages) > 0:
            self.conversation.result_messages[-1] = result
        else:
            self.conversation.result_messages.append(result)
        if new_hash is not None:
            self.last_hash = new_hash
        return self

    def add_user_message(self, *, message: UserMessage) -> Self:
        self.conversation.user_messages.append(message)
        return self


class FlowRun:
    def __init__(self) -> None:
        self._node_states: dict[tuple[str, int], str] = {}
        self._last_requested_indices: dict[str, int] = {}
        self._flow_name = ""
        self._id = ""
        self._agent: Agent | None = None
        self._flow_args: tuple[Any, ...] | None = None
        self._flow_kwargs: dict[str, Any] | None = None

    @property
    def flow_name(self) -> str:
        return self._flow_name

    @property
    def id(self) -> str:
        return self._id

    @property
    def agent(self) -> Agent:
        if self._agent is None:
            raise Honk("Agent is only accessible once a run is started")
        return self._agent

    @property
    def flow_inputs(self) -> tuple[tuple[Any, ...], dict[str, Any]]:
        if self._flow_args is None or self._flow_kwargs is None:
            raise Honk("This Flow run has not been executed before")

        return self._flow_args, self._flow_kwargs

    def get_all[R: Result](self, *, task: "Task[Any, R]") -> list[NodeState[R]]:
        matching_nodes: list[NodeState[R]] = []
        for key, node_state in self._node_states.items():
            if key[0] == task.name:
                matching_nodes.append(
                    NodeState[task.result_type].model_validate_json(node_state)
                )
        return sorted(matching_nodes, key=lambda node: node.index)

    def get[R: Result](self, *, task: "Task[Any, R]", index: int = 0) -> NodeState[R]:
        if (
            existing_node_state := self._node_states.get((task.name, index))
        ) is not None:
            return NodeState[task.result_type].model_validate_json(existing_node_state)
        else:
            return NodeState[task.result_type](
                task_name=task.name,
                index=index,
                conversation=Conversation[task.result_type](
                    user_messages=[], result_messages=[]
                ),
                last_hash=0,
            )

    def set_flow_inputs(self, *args: Any, **kwargs: Any) -> None:
        self._flow_args = args
        self._flow_kwargs = kwargs

    def add_node_state(self, node_state: NodeState[Any], /) -> None:
        key = (node_state.task_name, node_state.index)
        self._node_states[key] = node_state.model_dump_json()

    def get_next[R: Result](self, *, task: "Task[Any, R]") -> NodeState[R]:
        if task.name not in self._last_requested_indices:
            self._last_requested_indices[task.name] = 0
        else:
            self._last_requested_indices[task.name] += 1

        return self.get(task=task, index=self._last_requested_indices[task.name])

    def start(
        self,
        *,
        flow_name: str,
        run_id: str,
        agent_logger: IAgentLogger | None = None,
    ) -> None:
        self._last_requested_indices = {}
        self._flow_name = flow_name
        self._id = run_id
        self._agent = Agent(
            flow_name=self.flow_name, run_id=self.id, logger=agent_logger
        )

    def end(self) -> None:
        self._last_requested_indices = {}
        self._flow_name = ""
        self._id = ""
        self._agent = None

    def clear_node(self, *, task: "Task[Any, Result]", index: int) -> None:
        key = (task.name, index)
        if key in self._node_states:
            del self._node_states[key]

    def dump(self) -> SerializedFlowRun:
        flow_args, flow_kwargs = self.flow_inputs

        return SerializedFlowRun(
            json.dumps(
                {
                    "node_states": {
                        ":".join([task_name, str(index)]): value
                        for (task_name, index), value in self._node_states.items()
                    },
                    "flow_args": list(flow_args),
                    "flow_kwargs": flow_kwargs,
                }
            )
        )

    @classmethod
    def load(cls, serialized_flow_run: SerializedFlowRun, /) -> Self:
        flow_run = cls()
        run = json.loads(serialized_flow_run)

        new_node_states: dict[tuple[str, int], str] = {}
        for key, node_state in run["node_states"].items():
            task_name, index = tuple(key.split(":"))
            new_node_states[(task_name, int(index))] = node_state
        flow_run._node_states = new_node_states

        flow_run._flow_args = tuple(run["flow_args"])
        flow_run._flow_kwargs = run["flow_kwargs"]

        return flow_run


_current_flow_run: ContextVar[FlowRun | None] = ContextVar(
    "current_flow_run", default=None
)


class Flow[**P]:
    def __init__(
        self,
        fn: Callable[P, Awaitable[None]],
        /,
        *,
        name: str | None = None,
        store: IFlowRunStore | None = None,
        agent_logger: IAgentLogger | None = None,
    ) -> None:
        self._fn = fn
        self._name = name
        self._agent_logger = agent_logger
        self._store = store or InMemoryFlowRunStore(flow_name=self.name)

    @property
    def name(self) -> str:
        return self._name or self._fn.__name__

    @property
    def current_run(self) -> FlowRun:
        run = _current_flow_run.get()
        if run is None:
            raise Honk("No current flow run")
        return run

    @asynccontextmanager
    async def start_run(self, *, run_id: str) -> AsyncIterator[FlowRun]:
        existing_run = await self._store.get(run_id=run_id)
        if existing_run is None:
            run = FlowRun()
        else:
            run = existing_run

        old_run = _current_flow_run.get()
        _current_flow_run.set(run)

        run.start(flow_name=self.name, run_id=run_id, agent_logger=self._agent_logger)
        yield run
        await self._store.save(run=run)
        run.end()

        _current_flow_run.set(old_run)

    async def generate(self, *args: P.args, **kwargs: P.kwargs) -> None:
        flow_run = _current_flow_run.get()
        if flow_run is None:
            raise Honk("No current flow run")

        flow_run.set_flow_inputs(*args, **kwargs)
        await self._fn(*args, **kwargs)

    async def regenerate(self) -> None:
        flow_run = _current_flow_run.get()
        if flow_run is None:
            raise Honk("No current flow run")

        flow_args, flow_kwargs = flow_run.flow_inputs
        await self._fn(*flow_args, **flow_kwargs)


class Task[**P, R: Result]:
    def __init__(
        self,
        generator: Callable[P, Awaitable[R]],
        /,
        *,
        retries: int = 0,
        adapter_model: GeminiModel = GeminiModel.FLASH,
    ) -> None:
        self._generator = generator
        self._retries = retries
        self._adapter_model = adapter_model
        self._adapter_model = adapter_model

    @property
    def result_type(self) -> type[R]:
        result_type = self._generator.__annotations__.get("return")
        if result_type is None:
            raise Honk(f"Task {self.name} has no return type annotation")
        return result_type

    @property
    def name(self) -> str:
        return self._generator.__name__

    async def generate(
        self, state: NodeState[R], *args: P.args, **kwargs: P.kwargs
    ) -> R:
        state_hash = self.__hash_task_call(*args, **kwargs)
        if state_hash != state.last_hash:
            result = await self._generator(*args, **kwargs)
            state.add_result(result=result, new_hash=state_hash, overwrite=True)
            return result
        else:
            return state.result

    async def jam(
        self,
        *,
        user_message: UserMessage,
        context: SystemMessage | None = None,
        index: int = 0,
    ) -> R:
        flow_run = self.__get_current_flow_run()
        node_state = flow_run.get(task=self, index=index)

        if context is not None:
            node_state.set_context(context=context)
        node_state.add_user_message(message=user_message)

        result = await self.__adapt(
            conversation=node_state.conversation, agent=flow_run.agent
        )
        node_state.add_result(result=result)
        flow_run.add_node_state(node_state)

        return result

    async def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        flow_run = self.__get_current_flow_run()
        node_state = flow_run.get_next(task=self)
        result = await self.generate(node_state, *args, **kwargs)
        flow_run.add_node_state(node_state)
        return result

    async def __adapt(self, *, conversation: Conversation[R], agent: Agent) -> R:
        messages: list[UserMessage | AssistantMessage] = []
        for message_index in range(len(conversation.user_messages)):
            user_message = conversation.user_messages[message_index]
            result = conversation.result_messages[message_index]

            if isinstance(result, TextResult):
                assistant_text = result.text
            else:
                assistant_text = result.model_dump_json()
            assistant_message = AssistantMessage(text=assistant_text)
            messages.append(assistant_message)
            messages.append(user_message)

        return await agent(
            messages=messages,
            model=self._adapter_model,
            task_name=f"adapt--{self.name}",
            system=conversation.context,
            response_model=self.result_type,
        )

    def __hash_task_call(self, *args: P.args, **kwargs: P.kwargs) -> int:
        try:
            to_hash = str(
                tuple(args)
                + tuple(kwargs.values())
                + (self._generator.__code__, self._adapter_model)
            )
            return hash(to_hash)
        except TypeError:
            raise Honk(f"Unhashable argument to task {self.name}: {args} {kwargs}")

    def __get_current_flow_run(self) -> FlowRun:
        run = _current_flow_run.get()
        if run is None:
            raise Honk("No current flow run")
        return run


@overload
def task[**P, R: Result](generator: Callable[P, Awaitable[R]], /) -> Task[P, R]: ...
@overload
def task[**P, R: Result](
    *, retries: int = 0, adapter_model: GeminiModel = GeminiModel.FLASH
) -> Callable[[Callable[P, Awaitable[R]]], Task[P, R]]: ...
def task[**P, R: Result](
    generator: Callable[P, Awaitable[R]] | None = None,
    /,
    *,
    retries: int = 0,
    adapter_model: GeminiModel = GeminiModel.FLASH,
) -> Task[P, R] | Callable[[Callable[P, Awaitable[R]]], Task[P, R]]:
    if generator is None:

        def decorator(fn: Callable[P, Awaitable[R]]) -> Task[P, R]:
            return Task(fn, retries=retries, adapter_model=adapter_model)

        return decorator

    return Task(generator, retries=retries, adapter_model=adapter_model)


@overload
def flow[**P](fn: Callable[P, Awaitable[None]], /) -> Flow[P]: ...
@overload
def flow[**P](
    *,
    name: str | None = None,
    store: IFlowRunStore | None = None,
    agent_logger: IAgentLogger | None = None,
) -> Callable[[Callable[P, Awaitable[None]]], Flow[P]]: ...
def flow[**P](
    fn: Callable[P, Awaitable[None]] | None = None,
    /,
    *,
    name: str | None = None,
    store: IFlowRunStore | None = None,
    agent_logger: IAgentLogger | None = None,
) -> Flow[P] | Callable[[Callable[P, Awaitable[None]]], Flow[P]]:
    if fn is None:

        def decorator(fn: Callable[P, Awaitable[None]]) -> Flow[P]:
            return Flow(fn, name=name, store=store, agent_logger=agent_logger)

        return decorator

    return Flow(fn, name=name, store=store, agent_logger=agent_logger)
