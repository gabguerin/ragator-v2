"""RAGator state."""
from typing import Sequence, Optional

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from src.retrieval.chunk import Chunk


class StateSchema(BaseModel):
    """RAG state for the RAGator."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    question_classification: Optional[str] = Field(None)
    retrieved_chunks: Optional[list[Chunk]] = Field(None)
