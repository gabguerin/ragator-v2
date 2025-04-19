from pathlib import Path
from typing import List, Annotated, Sequence

import yaml
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel

from rag_graphs.ragator.paths import RAG_PARAMS_PATH
from src.retrieval.chunk import Chunk


class ChatModelParams(BaseModel):
    """This class is used to define the chat model."""

    module: str
    class_name: str
    model_name: str


class LLMInstructionParams(BaseModel):
    """
    This class is used to define the instruction for the LLM.
    """

    model: ChatModelParams
    system_prompt: str
    prompt_inputs: list[str]
    format_json: bool


class EmbeddingParams(BaseModel):
    """This class is used to define the embedding model."""
    module: str
    class_name: str
    model_name: str
    dimension: int


class VectorStoreParams(BaseModel):
    """This class is used to define the vector store."""
    module: str
    class_name: str
    collection_name: str


class RagParams(BaseModel):
    """
    This class is used to define the parameters for the RAG.
    """
    embedding: EmbeddingParams
    vector_store: VectorStoreParams
    llm_instructions: dict[str, LLMInstructionParams]


class Message(BaseModel):
    """This class is used to define a message."""

    user_question: str
    ai_answer: str
    question_classification: str | None


class RagState(BaseModel):
    rag_params_path: Path
    rag_params: RagParams
    # With the add_messages decorator, this will be a list of BaseMessage objects that will be updated after each node
    message_history: Annotated[Sequence[BaseMessage], add_messages]
    question_classification: str | None
    retrieved_chunks: List[Chunk]

    def model_post_init(self, __context) -> None:
        if self.rag_params is None and self.rag_params_path.exists():
            with open(self.rag_params_path, "r") as f:
                data = yaml.safe_load(f)
            self.rag_params = RagParams(**data)
