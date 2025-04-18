import uuid
from typing import List

from langchain_core.documents import Document
from qdrant_client import AsyncQdrantClient
from qdrant_client.grpc import PointStruct

from retrieval.vector_stores.base_vectorstore import BaseVectorStore


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
        """Add documents to the Qdrant collection."""
        vectors = [self.embedding_model(doc.page_content) for doc in documents]
        payloads = [doc.metadata for doc in documents]
        points = [
            PointStruct(id=str(uuid.uuid4()), vector=vec, payload=payload)
            for vec, payload in zip(vectors, payloads)
        ]

        await self.client.upsert(collection_name=self.collection_name, points=points)

    async def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Return documents most similar to the query."""
        query_vector = self.embedding_function(query)

        search_result = await self.client.search(
            collection_name=self.collection_name, query_vector=query_vector, limit=k
        )

        results = [
            Document(page_content=hit.payload.get("text", ""), metadata=hit.payload)
            for hit in search_result
        ]

        return results
