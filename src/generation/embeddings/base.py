from abc import ABC, abstractmethod
from typing import List


class BaseEmbeddingModel(ABC):
    """Abstract base class for embedding models."""

    def __init__(self, model_name: str, dimensions: int):
        self.model_name = model_name
        self.dimensions = dimensions

        self.client = self.initialize_client()

    @abstractmethod
    def initialize_client(self):
        """Initialize the client for the embedding model."""
        ...

    @abstractmethod
    async def embed_query(self, text: str) -> List[float]:
        """Embed a single query string."""
        ...

    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed a batch of strings."""
        ...
