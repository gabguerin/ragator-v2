from langchain_core.runnables import RunnableConfig

from src.generation.chat_models.base import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from src.graphs.ragator.config import ConfigSchema
from src.graphs.ragator.state import StateSchema
from src.utils.importlib import import_module_from_path


async def generate_llm_response_from_context(
    state: StateSchema, config: RunnableConfig
) -> dict:
    """Generate an answer using a language model based on the question classification."""

    # Load configuration
    config = ConfigSchema(**config["configurable"])

    # Load RAG chat model
    llm: BaseChatModel = import_module_from_path(
        module_path=config.rag_chat_model.module,
        object_name=config.rag_chat_model.class_name,
    )(model_name=config.rag_chat_model.model_name)

    # Retrieve the context based on the retrieved chunks
    context = "\n".join(
        [
            f"Source: {chunk.source}\n\n Content: {chunk.content}"
            for chunk in state.retrieved_chunks
        ]
    )

    response = await llm.invoke(
        [
            *state.messages[:-1],
            SystemMessage(content=config.rag_chat_model.system_prompt),
            HumanMessage(
                content=config.rag_chat_model.human_prompt.format(
                    context=context,
                    question=state.messages[-1].content,
                )
            ),
        ],
    )

    return {"messages": [AIMessage(content=response)]}
