from langchain_core.runnables import RunnableConfig

from src.generation.chat_models.base import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage

from src.graphs.ragator.state import StateSchema
from src.graph_config import ChatModelConfig
from src.utils.importlib import import_module_from_path


async def classify_question(state: StateSchema, config: RunnableConfig) -> dict:
    """Classify the question using a language model."""
    chat_model_config = ChatModelConfig(
        **config["configurable"]["classification_chat_model"]
    )

    llm: BaseChatModel = import_module_from_path(
        module_path=chat_model_config.module,
        object_name=chat_model_config.class_name,
    )(model_name=chat_model_config.model_name)

    question_classification = await llm.invoke(
        [
            SystemMessage(content=chat_model_config.system_prompt),
            HumanMessage(
                content=chat_model_config.human_prompt.format(
                    message_history="\n".join(
                        [f"{msg.type}: {msg.content}" for msg in state["messages"][:-1]]
                    )
                    or "",
                    question=state["messages"][-1].content,
                )
            ),
        ],
    )

    return {"question_classification": question_classification}
