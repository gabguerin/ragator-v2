from src.graphs.ragator.state import RagState
from src.generation.chat_models.base import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.params import RagParams
from src.utils.importlib import import_module_from_path


async def generate_llm_response(state: RagState) -> dict:
    """Generate a static answer using a language model to explain that the question is out of scope."""
    rag_params = RagParams(**state["rag_params"])

    if state.get("question_classification") == "OUT_OF_SCOPE":
        llm_instruction = rag_params.llm_instructions[
            "question_out_of_scope_instruction"
        ]
    elif state.get("question_classification") == "RAG":
        llm_instruction = rag_params.llm_instructions["question_about_rag_instruction"]
    else:
        raise ValueError("Invalid question classification")

    llm: BaseChatModel = import_module_from_path(
        module_path=llm_instruction.model.module,
        object_name=llm_instruction.model.class_name,
    )(model_name=llm_instruction.model.model_name)

    response = await llm.invoke(
        [
            SystemMessage(content=llm_instruction.system_prompt),
            HumanMessage(content=llm_instruction.human_prompt),
        ],
    )

    return {"messages": [AIMessage(content=response)]}
