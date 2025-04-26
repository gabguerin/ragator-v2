from langchain_core.runnables import RunnableConfig

from src.generation.chat_models.base import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage

from src.graphs.ragator.config import ConfigSchema
from src.graphs.ragator.state import StateSchema
from src.utils.importlib import import_module_from_path


async def classify_question(state: StateSchema, config: RunnableConfig) -> dict:
    """Classify the question using a language model."""
    
    # Load configuration
    config = ConfigSchema(**config["configurable"])

    # Load classification chat model
    llm: BaseChatModel = import_module_from_path(
        module_path=config.classification_chat_model.module,
        object_name=config.classification_chat_model.class_name,
    )(model_name=config.classification_chat_model.model_name)

    question_classification = await llm.invoke(
        [
            SystemMessage(content=config.classification_chat_model.system_prompt),
            HumanMessage(
                content=config.classification_chat_model.human_prompt.format(
                    message_history="\n".join(
                        [f"{msg.type}: {msg.content}" for msg in state.messages[:-1]]
                    )
                    or "",
                    question=state.messages[-1].content,
                )
            ),
        ],
    )

    return {"question_classification": question_classification}
