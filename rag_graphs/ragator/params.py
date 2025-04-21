from typing import List, Annotated, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel
from typing_extensions import TypedDict

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
    human_prompt: str


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
    retrieve_top_k: int


class RagParams(BaseModel):
    """
    This class is used to define the parameters for the RAG.
    """

    embedding: EmbeddingParams
    vector_store: VectorStoreParams
    llm_instructions: dict[str, LLMInstructionParams]


class RagState(TypedDict):
    # With the add operator, instead of updating the messages list, it will add the new messages to the list
    messages: Annotated[Sequence[BaseMessage], add_messages]
    rag_params: dict
    question_classification: str | None
    retrieved_chunks: List[Chunk]
