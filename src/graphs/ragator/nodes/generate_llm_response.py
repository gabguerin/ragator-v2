from langchain_core.runnables import RunnableConfig

from src.generation.chat_models.base import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from src.graphs.ragator.config import ConfigSchema
from src.graphs.ragator.state import StateSchema
from src.utils.importlib import import_module_from_path


async def generate_llm_response(state: StateSchema, config: RunnableConfig) -> dict:
    """Generate a static answer using a language model to explain that the question is out of scope."""

    # Load configuration
    config_params = ConfigSchema(**config["configurable"])

    # Load the appropriate chat model based on the question classification
    if state.question_classification == "OUT_OF_SCOPE":
        chat_model_config = config_params.question_out_of_scope_chat_model
    elif state.question_classification == "RAG":
        chat_model_config = config_params.question_about_rag_chat_model
    else:
        raise ValueError("Invalid question classification")

    llm: BaseChatModel = import_module_from_path(
        module_path=chat_model_config.module,
        object_name=chat_model_config.class_name,
    )(model_name=chat_model_config.model_name)

    response = await llm.invoke(
        [
            SystemMessage(content=chat_model_config.system_prompt),
            HumanMessage(content=chat_model_config.human_prompt),
        ],
    )

    return {"messages": [AIMessage(content=response)]}
