from rag_graphs.ragator.state import RagState
from src.generation.chat_models.base import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.params import RagParams
from src.utils.importlib import import_module_from_path


async def generate_llm_response_from_context(state: RagState) -> dict:
    """Generate an answer using a language model based on the question classification."""
    rag_params = RagParams(**state["rag_params"])
    llm_instruction = rag_params.llm_instructions["answer_rag_instruction"]

    llm: BaseChatModel = import_module_from_path(
        module_path=llm_instruction.model.module,
        object_name=llm_instruction.model.class_name,
    )(model_name=llm_instruction.model.model_name)

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
            SystemMessage(content=llm_instruction.system_prompt),
            HumanMessage(
                content=llm_instruction.human_prompt.format(
                    context=context,
                    question=state["messages"][-1].content,
                )
            ),
        ],
    )

    return {"messages": [AIMessage(content=response)]}
