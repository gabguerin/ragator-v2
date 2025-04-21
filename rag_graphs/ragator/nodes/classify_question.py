from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from rag_graphs.ragator.params import RagState, RagParams
from src.utils.importlib import import_module_from_path


def main(state: RagState) -> dict:
    """Classify the question using a language model."""
    rag_params = RagParams(**state["rag_params"])
    llm_instruction = rag_params.llm_instructions["question_classification_instruction"]

    llm: BaseChatModel = import_module_from_path(
        module_path=llm_instruction.model.module,
        object_name=llm_instruction.model.class_name,
    )(model=llm_instruction.model.model_name)

    response = llm.invoke(
        [
            SystemMessage(content=llm_instruction.system_prompt),
            HumanMessage(
                content=llm_instruction.human_prompt.format(
                    question=state["messages"][-1].content,
                )
            ),
        ],
    ).content

    return {"question_classification": response}
