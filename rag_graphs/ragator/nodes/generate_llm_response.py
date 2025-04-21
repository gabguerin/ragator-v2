from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from rag_graphs.ragator.params import RagState, RagParams
from src.utils.importlib import import_module_from_path


def generate_llm_response(state: RagState) -> dict:
    """Generate a static answer using a language model to explain that the question is out of scope."""
    rag_params = RagParams(**state["rag_params"])

    if state.get("question_classification") == "OUT_OF_SCOPE":
        llm_instruction = rag_params.llm_instructions["question_out_of_scope_instruction"]
    elif state.get("question_classification") == "RAG":
        llm_instruction = rag_params.llm_instructions["rag_instruction"]
    else:
        raise ValueError("Invalid question classification")

    llm: BaseChatModel = import_module_from_path(
        module_path=llm_instruction.model.module,
        object_name=llm_instruction.model.class_name,
    )(model=llm_instruction.model.model_name)

    response = llm.invoke(
        [
            SystemMessage(content=llm_instruction.system_prompt),
            HumanMessage(content=llm_instruction.human_prompt),
        ],
    ).content

    return {"messages": [AIMessage(response)]}
