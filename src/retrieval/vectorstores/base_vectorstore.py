from abc import ABC, abstractmethod
from typing import List

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from retrieval.files.base_file import BaseFile


class BaseVectorStore(ABC):
    def __init__(
        self,
        collection_name: str,
        embedding_model: Embeddings,
        local_path: str | None = None,
        url: str | None = None,
        api_key: str | None = None,
    ):
        """Initialize AsyncQdrantVectorStore."""
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.client = self.initialize_client(
            local_path=local_path, url=url, api_key=api_key
        )

    @abstractmethod
    def initialize_client(
        self,
        local_path: str | None = None,
        url: str | None = None,
        api_key: str | None = None,
    ):
        """Set up vector store client/connection."""
        pass

    @abstractmethod
    async def add_documents(self, documents: List[Document]):
        """Add or update documents in the vector store."""
        pass

    @abstractmethod
    async def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Retrieve top-k similar documents based on a query."""
        pass

    async def upsert_from_file(self, file: BaseFile):
        documents = await file.to_documents()
        await self.add_documents(documents)
