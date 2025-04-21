from rag_graphs.ragator.state import RagState
from src.generation.chat_models.base import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage
from src.params import RagParams
from src.utils.importlib import import_module_from_path


async def classify_question(state: RagState) -> dict:
    """Classify the question using a language model."""
    rag_params = RagParams(**state["rag_params"])
    llm_instruction = rag_params.llm_instructions["question_classification_instruction"]

    llm: BaseChatModel = import_module_from_path(
        module_path=llm_instruction.model.module,
        object_name=llm_instruction.model.class_name,
    )(model_name=llm_instruction.model.model_name)

    question_classification = await llm.invoke(
        [
            SystemMessage(content=llm_instruction.system_prompt),
            HumanMessage(
                content=llm_instruction.human_prompt.format(
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
