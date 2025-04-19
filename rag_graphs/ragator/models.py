from pathlib import Path
from typing import List

from pydantic import BaseModel

from rag_graphs.ragator.paths import RAG_PARAMS_PATH


class ChatModel(BaseModel):
    """This class is used to define the chat model."""

    module: str
    class_name: str
    model_name: str


class LLMInstruction(BaseModel):
    """
    This class is used to define the instruction for the LLM.
    """

    model: ChatModel
    system_prompt: str
    prompt_inputs: list[str]
    format_json: bool


class Embedding(BaseModel):
    """This class is used to define the embedding model."""
    module: str
    class_name: str
    model_name: str
    dimension: int


class VectorStore(BaseModel):
    """This class is used to define the vector store."""
    module: str
    class_name: str
    collection_name: str


class RagParams(BaseModel):
    """
    This class is used to define the parameters for the RAG.
    """
    embedding: Embedding
    vector_store: VectorStore
    llm_instructions: dict[str, LLMInstruction]


class RagState(BaseModel):
    rag_params_path: Path = RAG_PARAMS_PATH
    rag_params: RagParams
    message_history: list[str]
    question_classification: str | None
    context: List[str]
    answer: str | None
