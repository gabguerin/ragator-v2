from abc import ABC, abstractmethod
from typing import List, Dict, Any

from langchain_core.embeddings import Embeddings

from retrieval.file_handlers.file_handler import Chunk


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
        ...

    @abstractmethod
    async def create_or_overwrite_collection_if_exists(
            self, collection_name: str, vector_size: int
    ) -> None:
        ...

    @abstractmethod
    async def delete_collection(self, collection_name: str) -> None:
        ...

    @abstractmethod
    async def upsert_points(
        self,
        collection_name: str,
        chunks: List[Chunk],
        batch_size: int = 128,
    ) -> None:
        ...

    @abstractmethod
    async def similarity_search(
        self, collection_name: str, query: str, k: int
    ) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    async def delete_point(self, collection_name: str, point_id: str):
        ...
