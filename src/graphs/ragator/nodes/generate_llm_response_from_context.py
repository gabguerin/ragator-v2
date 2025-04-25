from langchain_core.runnables import RunnableConfig

from src.generation.chat_models.base import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from src.graphs.ragator.state import StateSchema
from src.graph_config import ChatModelConfig
from src.utils.importlib import import_module_from_path


async def generate_llm_response_from_context(
    state: StateSchema, config: RunnableConfig
) -> dict:
    """Generate an answer using a language model based on the question classification."""
    chat_model_config = ChatModelConfig(
        **config["configurable"]["rag_chat_model"]
    )

    llm: BaseChatModel = import_module_from_path(
        module_path=chat_model_config.module,
        object_name=chat_model_config.class_name,
    )(model_name=chat_model_config.model_name)

    # Retrieve the context based on the retrieved chunks
    context = "\n".join(
        [
            f"Source: {chunk.source}\n\n Content: {chunk.content}"
            for chunk in state["retrieved_chunks"]
        ]
    )

    response = await llm.invoke(
        [
            *state["messages"][:-1],
            SystemMessage(content=chat_model_config.system_prompt),
            HumanMessage(
                content=chat_model_config.human_prompt.format(
                    context=context,
                    question=state["messages"][-1].content,
                )
            ),
        ],
    )

    return {"messages": [AIMessage(content=response)]}
