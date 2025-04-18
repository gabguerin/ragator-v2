import os
from asyncio.log import logger

from dotenv import load_dotenv
from qdrant_client import AsyncQdrantClient
from qdrant_client.grpc import PointStruct

from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any

from tqdm import tqdm

from retrieval.file_handlers.file_handler import Chunk
from retrieval.vector_stores.base_store import BaseVectorStore

load_dotenv()


class QdrantStore(BaseVectorStore):
    """Wrapper around QdrantClient to index chunks and query them."""

    def initialize_client(self, *args, **kwargs) -> Any:
        return AsyncQdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )

    async def create_collection(self, collection_name: str, vector_size: int = 384):
        await self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    async def create_or_overwrite_collection_if_exists(
        self, collection_name: str, vector_size: int
    ) -> None:
        """Create a collection or overwrite if it already exists."""
        if await self.client.collection_exists(collection_name):
            logger.info(
                f"Deleting collection {collection_name} as it already exists"
            )
            await self.delete_collection(collection_name)

        logger.info(f"Creating collection {collection_name}")
        await self.create_collection(
            collection_name=collection_name,
            vector_size=vector_size,
        )

    async def delete_collection(self, name: str) -> None:
        await self.client.delete_collection(collection_name=name)

    async def upsert_points(
        self,
        collection_name: str,
        chunks: List[Chunk],
        batch_size: int = 128,
    ):
        for batch_start_index in tqdm(
            range(0, len(chunks), batch_size),
            desc=f"Adding documents to qdrant by batches of {batch_size}",
        ):
            chunks_batch = chunks[batch_start_index: batch_start_index + batch_size]

            # Embed the batch
            embeddings = await self.embedding_model.aembed_documents(
                [chunk.content for chunk in chunks_batch]
            )

            # Create points
            points = [
                PointStruct(
                    id=chunk.uuid,
                    vector=embedding,
                    payload=chunk.model_dump(exclude={"uuid"}))
                for chunk, embedding in zip(chunks_batch, embeddings)
            ]

            # Upsert into Qdrant
            await self.client.upsert(collection_name=collection_name, points=points)

    async def similarity_search(
        self, collection_name: str, query: str, k: int = 5
    ) -> List[Dict[str, Any]]:
        query_vector = await self.embedding_model.aembed_query(query)

        results = await self.client.search(
            collection_name=collection_name, query_vector=query_vector, limit=k
        )

        return [
            {
                "id": hit.id,
                "score": hit.score,
                "chunk_content": hit.payload["content"],
                "metadata": hit.payload["metadata"],
            }
            for hit in results
        ]

    async def delete_point(self, collection_name: str, point_id: str):
        await self.client.delete(
            collection_name=collection_name, points_selector={"points": [point_id]}
        )
