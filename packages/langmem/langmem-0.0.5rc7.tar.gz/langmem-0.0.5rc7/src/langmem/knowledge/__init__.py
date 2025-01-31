import asyncio
import typing
import uuid

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.store.base import SearchItem
from langgraph.prebuilt import ToolNode
from langgraph.utils.config import get_store
from pydantic import BaseModel
from trustcall import create_extractor
from langmem import utils
from langmem.knowledge.tools import create_search_memory_tool, create_manage_memory_tool
import langsmith as ls

## LangGraph Tools


def create_thread_extractor(
    model: str,
    schema: typing.Union[None, BaseModel, type] = None,
    instructions: str = "You are tasked with summarizing the following conversation.",
):
    """Creates a conversation thread summarizer using schema-based extraction.

    This function creates an asynchronous callable that takes conversation messages and produces
    a structured summary based on the provided schema. If no schema is provided, it uses a default
    schema with title and summary fields.

    Args:
        model: The chat model to use for summarization (name or instance)
        schema: Optional Pydantic model for structured output. Defaults to a simple
            summary schema with title and summary fields.
        instructions: System prompt template for the summarization task

    Returns:
        Async callable that takes a list of messages and returns a structured summary

    Example:
        >>> summarizer = create_thread_extractor("gpt-4")
        >>> messages = [
        ...     HumanMessage(content="Hi, I'm having trouble with my account"),
        ...     AIMessage(content="I'd be happy to help. What seems to be the issue?"),
        ...     HumanMessage(content="I can't reset my password")
        ... ]
        >>> summary = await summarizer(messages)
        >>> print(summary.title)
        "Password Reset Assistance"
        >>> print(summary.summary)
        "User reported issues with password reset process..."
    """

    class SummarizeThread(BaseModel):
        """Summarize the thread."""

        title: str
        summary: str

    schema_ = schema or SummarizeThread
    extractor = create_extractor(model, tools=[schema_], tool_choice="any")

    async def summarize_conversation(messages: list[AnyMessage]):
        id_ = str(uuid.uuid4())
        messages = [
            {"role": "system", "content": instructions},
            {
                "role": "user",
                "content": f"Summarize the conversation below:\n\n"
                f"<conversation_{id_}>\n{utils.get_conversation}\n</conversation_{id_}>",
            },
        ]
        response = await extractor.ainvoke(messages)
        result = response["responses"][0]
        if isinstance(result, schema_):
            return result
        return result.model_dump(mode="json")

    return summarize_conversation


_MEMORY_INSTRUCTIONS = """You are tasked with extracting or upserting memories for all entities, concepts, etc.

Extract all important facts or entities. If an existing MEMORY is incorrect or outdated, update it based on the new information.
"""


@typing.overload
def create_memory_enricher(
    model: str | BaseChatModel,
    /,
    instructions: str = _MEMORY_INSTRUCTIONS,
    enable_inserts: bool = True,
    enable_deletes: bool = False,
    schemas: None = None,
) -> typing.Callable[
    [list[AnyMessage], typing.Optional[list[str]]], typing.Awaitable[tuple[str, str]]
]: ...


@typing.overload
def create_memory_enricher(
    model: str | BaseChatModel,
    /,
    schemas: list,
    instructions: str = _MEMORY_INSTRUCTIONS,
    enable_inserts: bool = True,
    enable_deletes: bool = False,
) -> typing.Callable[
    [
        list[AnyMessage],
        typing.Optional[
            typing.Union[
                list[tuple[str, BaseModel]],
                list[tuple[str, str, dict]],
            ]
        ],
    ],
    typing.Awaitable[tuple[str, BaseModel]],
]: ...


def create_memory_enricher(  # type: ignore
    model: str | BaseChatModel,
    /,
    schemas: list | None = None,
    instructions: str = _MEMORY_INSTRUCTIONS,
    enable_inserts: bool = True,
    enable_deletes: bool = False,
):
    """Creates a memory management component that extracts and updates entities from conversations.

    This function builds an asynchronous memory enricher that can extract structured information
    from conversations, update existing memories, and optionally remove outdated information.
    It supports both default string-based memories and custom schema-based memory types.

    Args:
        model: Chat model instance or name for memory extraction
        schemas: List of Pydantic models defining memory types to extract. If None,
            uses a simple string-based memory schema.
        instructions: System prompt template for memory extraction
        enable_inserts: Allow creating new memory entries
        enable_deletes: Allow removing outdated memories

    Returns:
        Async callable that takes messages and existing memories, returns updated memories

    Examples:
        Basic usage with string memories:
        >>> enricher = create_memory_enricher("gpt-4")
        >>> messages = [HumanMessage(content="I love sushi and live in New York")]
        >>> memories = await enricher(messages)
        >>> print(memories[0].content)
        "User loves sushi and resides in New York"

        With custom schema:
        >>> class Preference(BaseModel):
        ...     category: str
        ...     items: list[str]
        >>> enricher = create_memory_enricher("claude-3", schemas=[Preference])
        >>> memories = await enricher(messages, existing=[])
        >>> print(memories[0].items)
        ['sushi']
    """
    model = model if isinstance(model, BaseChatModel) else init_chat_model(model)
    str_type = False
    if schemas is None:

        class Memory(BaseModel):
            """Call this tool to extract memories for things like preferences, instructions, important context, events, and anything else you want to remember about for future conversations."""

            content: str

        schemas = [Memory]
        str_type = True

    @ls.traceable
    async def enrich_memories(
        messages: list[AnyMessage],
        existing: typing.Optional[
            typing.Union[
                list[str],
                list[tuple[str, BaseModel]],
                list[tuple[str, str, dict]],
            ]
        ] = None,
    ):
        id_ = str(uuid.uuid4())
        session = (
            f"\n\n<session_{id_}>\n{utils.get_conversation(messages)}\n</session_{id_}>"
            if messages
            else ""
        )
        coerced = [
            {"role": "system", "content": instructions},
            {
                "role": "user",
                "content": f"Enrich, prune, and organize memories based on any new information."
                " If an existing memory is incorrect or outdated, update it based on the new information. "
                "All operations must be done in single parallel call."
                f"{session}",
            },
        ]
        if str_type and existing and all(isinstance(ex, str) for ex in existing):
            existing = [
                (str(uuid.uuid4()), "Memory", Memory(content=ex)) for ex in existing
            ]
        existing = [
            (
                tuple(e)
                if isinstance(e, (tuple, list)) and len(e) == 3
                else (
                    e[0],
                    e[1].__repr_name__() if isinstance(e[1], BaseModel) else "__any__",
                    e[1],
                )
            )
            for e in existing
        ]

        extractor = create_extractor(
            model,
            tools=schemas,
            tool_choice="any",
            enable_inserts=enable_inserts,
            enable_deletes=enable_deletes,
            # For now, don't fail on existing schema mismatches
            existing_schema_policy=False,
        )
        response = await extractor.ainvoke({"messages": coerced, "existing": existing})
        return [
            (rmeta.get("json_doc_id", str(uuid.uuid4())), r)
            for r, rmeta in zip(response["responses"], response["response_metadata"])
        ]

    return enrich_memories


def create_memory_searcher(
    model: str | BaseChatModel,
    prompt: str = "You are a memory search assistant.",
    *,
    namespace_prefix: tuple[str, ...] = ("memories", "{user_id}"),
):
    """Creates a memory search pipeline with automatic query generation.

    This function builds a pipeline that combines query generation, memory search,
    and result ranking into a single component. It uses the provided model to
    generate effective search queries based on conversation context.

    Args:
        model: Chat model for generating search queries
        prompt: System prompt template for search assistant
        namespace_prefix: Tuple defining storage namespace structure. Default is
            ("memories", "{user_id}") which organizes memories by user.

    Returns:
        Runnable pipeline that takes messages and returns sorted memory artifacts,
        ranked by relevance score.

    Example:
        >>> searcher = create_memory_searcher("gpt-3.5-turbo")
        >>> messages = [HumanMessage(content="What do I like to eat?")]
        >>> results = await searcher.ainvoke({"messages": messages})
        >>> print(results[0].value["content"])
        "User enjoys sushi and Italian cuisine"
    """
    template = ChatPromptTemplate.from_messages(
        [
            ("system", prompt),
            ("placeholder", "{messages}"),
            ("user", "Search for memories relevant to the above context."),
        ]
    )
    model = model if isinstance(model, BaseChatModel) else init_chat_model(model)
    search_tool = create_search_memory_tool(namespace_prefix=namespace_prefix)
    query_gen = model.bind_tools(
        [search_tool],
        tool_choice="search_memory",
    )

    def return_sorted(tool_messages: list):
        artifacts = {
            (*item.namespace, item.key): item
            for msg in tool_messages
            for item in (msg.artifact or [])
        }
        return [
            v
            for v in sorted(
                artifacts.values(),
                key=lambda item: item.score if item.score is not None else 0,
                reverse=True,
            )
        ]

    return (
        template
        | utils.merge_message_runs
        | query_gen
        | (lambda msg: [msg])
        | ToolNode([search_tool])
        | return_sorted
    ).with_config({"run_name": "search_memory_pipeline"})


class MemoryPhase(TypedDict, total=False):
    instructions: str
    include_messages: bool
    enable_inserts: bool
    enable_deletes: bool


def create_memory_store_enricher(
    model: str | BaseChatModel,
    *,
    schemas: list | None = None,
    instructions: str = _MEMORY_INSTRUCTIONS,
    enable_inserts: bool = True,
    enable_deletes: bool = True,
    query_model: str | BaseChatModel | None = None,
    namespace_prefix: tuple[str, ...] = ("memories", "{user_id}"),
    query_limit: int = 100,
    phases: list[MemoryPhase] | None = None,
):
    """End-to-end memory management system with automatic storage integration.

    This function creates a comprehensive memory management system that combines:
    1. Automatic memory search based on conversation context
    2. Memory extraction and enrichment
    3. Persistent storage operations

    The system can automatically update existing memories when new information
    contradicts or supplements them, and optionally remove outdated information.

    Args:
        model: Primary model for memory extraction/updates
        schemas: dicts or Pydantic models defining memory types. If None, uses string-based memories.
        instructions: System prompt for memory management
        enable_inserts: Allow new memory creation
        enable_deletes: Allow memory removal
        query_model: Optional separate model for search queries. If None, uses primary model.
        namespace_prefix: Storage namespace structure for organizing memories

    Returns:
        Async callable that manages full memory lifecycle from conversation input to storage

    Example:
        >>> memory_manager = create_memory_store_enricher("gpt-4")
        >>> messages = [
        ...     HumanMessage(content="I've moved to Paris from New York"),
        ...     AIMessage(content="Got it, updating your location information")
        ... ]
        >>> await memory_manager(messages)  # Updates location memory
        >>> # If enable_deletes=True, also removes outdated New York location
    """
    model = model if isinstance(model, BaseChatModel) else init_chat_model(model)
    query_model = (
        model
        if query_model is None
        else (
            query_model
            if isinstance(query_model, BaseChatModel)
            else init_chat_model(query_model)
        )
    )

    first_pass_enricher = create_memory_enricher(
        model,
        schemas=schemas,
        instructions=instructions,
        enable_inserts=enable_inserts,
        enable_deletes=enable_deletes,
    )

    def build_phase_enricher(phase: MemoryPhase):
        return create_memory_enricher(
            model,
            schemas=schemas,
            instructions=phase.get(
                "instructions",
                "You are a memory manager. Deduplicate, consolidate, and enrich these memories.",
            ),
            enable_inserts=phase.get("enable_inserts", True),
            enable_deletes=phase.get("enable_deletes", True),
        )

    def apply_enricher_output(
        enricher_output: list[tuple[str, BaseModel]],
        store_based: list[tuple[str, str, dict]],
        store_map: dict[str, SearchItem],
        ephemeral: list[tuple[str, str, dict]],
    ):
        store_dict = {
            st_id: (st_id, kind, content) for (st_id, kind, content) in store_based
        }
        ephemeral_dict = {
            st_id: (st_id, kind, content) for (st_id, kind, content) in ephemeral
        }

        removed_ids = []

        for stable_id, model_data in enricher_output:
            if model_data.__repr_name__() == "RemoveDoc":
                removal_id = model_data.json_doc_id
                if removal_id and removal_id in store_map:
                    print(
                        f"Popping permanent memory {removal_id}",
                        removal_id in store_dict,
                        flush=True,
                    )
                    removed_ids.append(removal_id)
                else:
                    print(
                        f"Popping ephemeral memory {removal_id}",
                        removal_id in ephemeral,
                        flush=True,
                    )
                store_dict.pop(removal_id, None)
                ephemeral_dict.pop(removal_id, None)
                continue

            new_content = model_data.model_dump(mode="json")  # Could maybe just keep
            new_kind = model_data.__repr_name__()
            if not new_kind:
                new_kind = "Memory"

            if stable_id in store_dict:
                st_id, _, _ = store_dict[stable_id]
                store_dict[stable_id] = (st_id, new_kind, new_content)
            elif stable_id in ephemeral_dict:
                st_id, _, _ = ephemeral_dict[stable_id]
                ephemeral_dict[stable_id] = (st_id, new_kind, new_content)
            else:
                ephemeral_dict[stable_id] = (stable_id, new_kind, new_content)
        return list(store_dict.values()), list(ephemeral_dict.values()), removed_ids

    search_tool = create_search_memory_tool(namespace_prefix=namespace_prefix)
    query_gen = query_model.bind_tools([search_tool], tool_choice="auto")
    namespacer = utils.NamespaceTemplate(namespace_prefix)

    async def manage_memories(messages: list[AnyMessage]):
        store = get_store()
        namespace = namespacer()
        convo = utils.get_conversation(messages)

        # Ask the model which store-based memories might be relevant
        search_req = await query_gen.ainvoke(
            f"Use parallel tool calling to search for distinct memories or aspects that would be relevant to this conversation::\n\n<convo>\n{convo}\n</convo>."
        )
        all_search_results = await asyncio.gather(
            *(
                store.asearch(namespace, **(tc["args"] | {"limit": query_limit}))
                for tc in search_req.tool_calls
            )
        )

        search_results = {}
        for results in all_search_results:
            for it in results:
                search_results[(it.namespace, it.key)] = it

        sorted_results = sorted(
            search_results.values(),
            key=lambda it: it.score if it.score is not None else float("-inf"),
            reverse=True,
        )[:query_limit]

        store_map: dict[str, SearchItem] = {}
        for item in sorted_results:
            stable_id = uuid.uuid5(
                uuid.NAMESPACE_DNS, str((*item.namespace, item.key))
            ).hex
            store_map[stable_id] = item

        store_based = []  # Original items that are found in the store
        for st_id, artifact in store_map.items():
            val = artifact.value
            store_based.append((st_id, val["kind"], val["content"]))

        ephemeral: list[tuple[str, str, dict]] = []
        removed_store_ids: set[str] = set()

        first_pass_result = await first_pass_enricher(messages, existing=store_based)
        store_based, ephemeral, newly_removed = apply_enricher_output(
            first_pass_result, store_based, store_map, ephemeral
        )
        for rid in newly_removed:
            removed_store_ids.add(rid)

        if phases:
            for phase in phases:
                enricher = build_phase_enricher(phase)
                phase_messages = (
                    messages if phase.get("include_messages", False) else []
                )
                phase_result = await enricher(
                    phase_messages, existing=store_based + ephemeral
                )

                store_based, ephemeral, newly_removed = apply_enricher_output(
                    phase_result, store_based, store_map, ephemeral
                )
                for rid in newly_removed:
                    removed_store_ids.add(rid)

        final_mem = store_based + ephemeral

        final_puts = []
        for st_id, kind, content in final_mem:
            if st_id in removed_store_ids:
                continue
            if st_id in store_map:
                old_art = store_map[st_id]
                changed = (
                    old_art.value["kind"] != kind or old_art.value["content"] != content
                )
                if changed:
                    # Updates
                    final_puts.append(
                        {
                            "namespace": old_art.namespace,
                            "key": old_art.key,
                            "value": {
                                "kind": kind,
                                "content": content,
                            },
                        }
                    )
            else:
                # New inserts
                final_puts.append(
                    {
                        "namespace": namespace,
                        "key": st_id,
                        "value": {
                            "kind": kind,
                            "content": content,
                        },
                    }
                )

        final_deletes = []
        for st_id in removed_store_ids:
            if st_id in store_map:
                art = store_map[st_id]
                final_deletes.append((art.namespace, art.key))

        await asyncio.gather(
            *(store.aput(**put) for put in final_puts),
            *(store.adelete(ns, key) for (ns, key) in final_deletes),
        )

        return final_puts

    return manage_memories


__all__ = [
    "create_manage_memory_tool",
    "create_memory_enricher",
    "create_memory_searcher",
    "create_memory_store_enricher",
    "create_thread_extractor",
]
