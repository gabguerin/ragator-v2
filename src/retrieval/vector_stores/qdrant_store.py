from langchain_core.embeddings import Embeddings
from qdrant_client import AsyncQdrantClient
from qdrant_client.grpc import PointStruct

from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any
import uuid


class AsyncQdrantStore:
    def __init__(
        self, embedding_model: Embeddings, host: str = "localhost", port: int = 6333
    ):
        self.client = AsyncQdrantClient(host=host, port=port)
        self.embedder = embedding_model

    async def embed_text(self, texts: List[str]) -> List[List[float]]:
        return self.embedder.embed_documents(texts)

    async def create_collection(
        self, collection_name: str, vector_size: int = 384, distance: str = "Cosine"
    ):
        await self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance[distance]),
        )

    async def create_collection_if_not_exists(
        self, collection_name: str, vector_size: int = 384, distance: str = "Cosine"
    ):
        if not await self.client.collection_exists(collection_name=collection_name):
            await self.create_collection(
                collection_name=collection_name,
                vector_size=vector_size,
                distance=distance,
            )

    async def delete_collection(self, name: str):
        await self.client.delete_collection(collection_name=name)

    async def insert_documents(
        self,
        collection_name: str,
        texts: List[str],
        metadata: List[Dict[str, Any]] = None,
    ):
        embeddings = await self.embed_text(texts)
        metadata = metadata or [{} for _ in texts]

        points = [
            PointStruct(id=str(uuid.uuid4()), vector=vector, payload=data)
            for vector, data in zip(embeddings, metadata)
        ]

        await self.client.upsert(collection_name=collection_name, points=points)

    async def similarity_search(
        self, collection_name: str, query: str, k: int = 5
    ) -> List[Dict[str, Any]]:
        query_vector = await self.embedder.aembed_query(query)

        results = await self.client.query_points(
            collection_name=collection_name, query_vector=query_vector, limit=k
        )

        return [
            {"id": hit.id, "score": hit.score, "payload": hit.payload}
            for hit in results
        ]

    async def update_document(
        self,
        collection_name: str,
        point_id: str,
        new_text: str,
        new_metadata: Dict[str, Any] = None,
    ):
        new_vector = await self.embedder.aget_query_embedding(new_text)
        new_payload = new_metadata or {}

        await self.client.upsert(
            collection_name=collection_name,
            points=[PointStruct(id=point_id, vector=new_vector, payload=new_payload)],
        )

    async def delete_document(self, collection_name: str, point_id: str):
        await self.client.delete(
            collection_name=collection_name, points_selector={"points": [point_id]}
        )
