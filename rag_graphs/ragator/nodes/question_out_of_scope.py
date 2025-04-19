from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from rag_graphs.ragator.params import RagState
from src.utils.importlib import import_module_from_path


def main(state: RagState):
    """Generate a static answer using a language model to explain that the question is out of scope."""
    llm_instruction = state.rag_params.llm_instructions["question_out_of_scope_instruction"]

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

    return {"messages": AIMessage(response)}
