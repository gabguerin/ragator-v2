"""QdrantStore class for managing a Qdrant vector store."""
import os
from asyncio.log import logger

from dotenv import load_dotenv
from qdrant_client import AsyncQdrantClient
from qdrant_client.grpc import PointStruct

from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any

from tqdm import tqdm

from src.retrieval.chunk import Chunk
from src.retrieval.vector_stores.base_store import BaseVectorStore

load_dotenv()


class QdrantStore(BaseVectorStore):
    """Wrapper around QdrantClient to index chunks and query them."""

    def initialize_client(self) -> AsyncQdrantClient:
        """
        Initialize the Qdrant client.

        Returns:
            An instance of AsyncQdrantClient.
        """
        logger.info("Initializing Qdrant client.")
        return AsyncQdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )

    async def create_collection(self, collection_name: str, vector_size: int = 384):
        """
        Create a new collection in Qdrant.

        Args:
            collection_name (str): Name of the collection to create.
            vector_size (int): Size of the vectors to store in the collection.
        """
        logger.info(
            f"Creating collection '{collection_name}' with vector size {vector_size}."
        )
        await self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    async def create_or_overwrite_collection_if_exists(
        self, collection_name: str, vector_size: int
    ) -> None:
        """
        Create a collection or overwrite it if it already exists.

        Args:
            collection_name (str): Name of the collection.
            vector_size (int): Size of the vectors to store in the collection.
        """
        if await self.client.collection_exists(collection_name):
            logger.info(f"Collection '{collection_name}' exists. Deleting it.")
            await self.delete_collection(collection_name)

        logger.info(f"Creating collection '{collection_name}'.")
        await self.create_collection(
            collection_name=collection_name,
            vector_size=vector_size,
        )

    async def delete_collection(self, name: str) -> None:
        """
        Delete a collection from Qdrant.

        Args:
            name (str): Name of the collection to delete.
        """
        logger.info(f"Deleting collection '{name}'.")
        await self.client.delete_collection(collection_name=name)

    async def upsert_chunks(
        self,
        collection_name: str,
        chunks: List[Chunk],
        batch_size: int = 128,
    ):
        """
        Upsert points into a Qdrant collection in batches.

        Args:
            collection_name (str): Name of the collection to upsert points into.
            chunks (List[Chunk]): List of chunks to upsert.
            batch_size (int): Number of chunks to process in each batch.
        """
        for batch_start_index in tqdm(
            range(0, len(chunks), batch_size),
            desc=f"Upserting chunks to qdrant collection {collection_name} by batches of {batch_size}",
        ):
            chunks_batch = chunks[batch_start_index : batch_start_index + batch_size]

            embeddings = await self.embedding_model.aembed_documents(
                [chunk.content for chunk in chunks_batch]
            )

            points = [
                PointStruct(
                    id=chunk.uuid,
                    vector=embedding,
                    payload=chunk.model_dump(exclude={"uuid"}),
                )
                for chunk, embedding in zip(chunks_batch, embeddings)
            ]

            await self.client.upsert(collection_name=collection_name, points=points)

    async def similarity_search(
        self, collection_name: str, query: str, k: int = 5
    ) -> List[Chunk]:
        """
        Perform a similarity search in a Qdrant collection.

        Args:
            collection_name (str): Name of the collection to search.
            query (str): Query string to search for.
            k (int): Number of top results to return.

        Returns:
            List[Dict[str, Any]]: List of search results with metadata.
        """
        query_vector = await self.embedding_model.aembed_query(query)

        results = await self.client.search(
            collection_name=collection_name, query_vector=query_vector, limit=k
        )

        return [
            Chunk(
                uuid=hit.payload["uuid"],
                score=hit.score,
                content=hit.payload["content"],
                source=hit.payload["source"],
            )
            for hit in results
        ]

    async def delete_point(self, collection_name: str, point_id: str):
        """
        Delete a specific point from a Qdrant collection.

        Args:
            collection_name (str): Name of the collection.
            point_id (str): ID of the point to delete.
        """
        logger.info(
            f"Deleting point with ID '{point_id}' from collection '{collection_name}'."
        )
        await self.client.delete(
            collection_name=collection_name, points_selector={"points": [point_id]}
        )
