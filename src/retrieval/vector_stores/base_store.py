"""Abstract base class for vector stores."""
from abc import ABC, abstractmethod
from typing import List, Any

from langchain_core.embeddings import Embeddings

from retrieval.chunks.base_chunk import Chunk


class BaseVectorStore(ABC):
    """Abstract base class for vector stores."""

    def __init__(self, embedding_model: Embeddings):
        self.embedding_model = embedding_model
        self.client = self.initialize_client()

    @abstractmethod
    def initialize_client(self, *args, **kwargs) -> Any:
        """Initialize the vector store client."""
        ...

    @abstractmethod
    async def create_collection(self, collection_name: str, vector_size: int) -> None:
        """Create a new collection in the vector store."""
        ...

    @abstractmethod
    async def create_or_overwrite_collection_if_exists(
        self, collection_name: str, vector_size: int
    ) -> None:
        """Create a collection or overwrite it if it already exists."""
        ...

    @abstractmethod
    async def delete_collection(self, collection_name: str) -> None:
        """Delete a collection from the vector store."""
        ...

    @abstractmethod
    async def upsert_chunks(
        self,
        collection_name: str,
        chunks: List[Chunk],
        batch_size: int = 128,
    ) -> None:
        ...

    @abstractmethod
    async def similarity_search(
        self, collection_name: str, query: str, k: int
    ) -> List[Chunk]:
        ...

    @abstractmethod
    async def delete_point(self, collection_name: str, point_id: str):
        ...
