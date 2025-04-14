from typing import List

from langchain_core.documents import Document
from qdrant_client import AsyncQdrantClient
from langchain.vectorstores.qdrant import Qdrant

from retrieval.vectorstores.base_vectorstore import BaseVectorStore


class QdrantVectorStore(BaseVectorStore):
    """Wrapper around QdrantClient to index chunks and query them."""

    def initialize_client(
        self,
        local_path: str | None = None,
        url: str | None = None,
        api_key: str | None = None,
        timeout: int | None = None,
    ):
        """Initialize AsyncQdrantVectorStore."""
        return AsyncQdrantClient(
            path=local_path,
            url=url,
            api_key=api_key,
            timeout=timeout,
            prefer_grpc=False,
        )

    async def add_documents(self, documents: List[Document]):
        qdrant = await Qdrant.afrom_documents(
            documents=documents,
            embedding=self.embedding_model,
            collection_name=self.collection_name,
            client=self.client,
        )
        return qdrant

    async def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        qdrant = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embedding_model,
        )
        return await qdrant.asimilarity_search(query, k=k)
