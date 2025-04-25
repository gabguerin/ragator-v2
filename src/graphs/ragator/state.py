"""RAGator state."""
from typing import Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from typing_extensions import TypedDict, Annotated

from src.retrieval.chunk import Chunk


class StateSchema(TypedDict):
    """RAG state for the RAGator."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    question_classification: str | None
    retrieved_chunks: list[Chunk] | None
