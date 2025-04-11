"""Qdrant database wrapper to index and query document chunks."""

from __future__ import annotations

from typing import TYPE_CHECKING

import backoff
from langfuse.decorators import observe
from loguru import logger
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.models import Distance, PointStruct, VectorParams
from tqdm import tqdm

from src.constants import (
    PARQUET_CHUNK_ID_COLUMN,
    PARQUET_EMBEDDING_COLUMN,
    VECTOR_STORE_COLLECTION_NAME,
)
from src.models import SearchResult
from src.vector_store.vector_store import AsyncVectorStore

if TYPE_CHECKING:
    import pandas as pd
    from langchain.embeddings.base import Embeddings

    from src.settings import ProjectSettings


class AsyncQdrantVectorStore(AsyncVectorStore):
    """Wrapper around QdrantClient to index chunks and query them."""

    def __init__(
        self,
        collection_name: str = VECTOR_STORE_COLLECTION_NAME,
        local_path: str | None = None,
        url: str | None = None,
        api_key: str | None = None,
        timeout: int | None = None,
    ):
        """Initialize AsyncQdrantVectorStore."""
        self.client = AsyncQdrantClient(
            path=local_path,
            url=url,
            api_key=api_key,
            timeout=timeout,
            prefer_grpc=False,
        )
        self.collection_name = collection_name

    @observe(name="create collection")  # type: ignore
    async def create_or_overwrite_collection_if_exists(
        self, embedding_size: int
    ) -> None:
        """Create a collection. Overwrite it already exists."""
        if await self.client.collection_exists(self.collection_name):
            logger.info(
                f"Deleting collection {self.collection_name} as it already exists"
            )
            await self.client.delete_collection(self.collection_name)

        logger.info(f"Creating collection {self.collection_name}")
        await self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=embedding_size, distance=Distance.COSINE, on_disk=True
            ),
        )

    @observe(name="add documents")  # type: ignore
    async def add_documents_to_vector_store(
        self,
        documents_to_add: pd.DataFrame,
        metadata_keys: tuple[str, ...],
        batch_size: int = 128,
    ) -> None:
        """Add new documents to the vector store.

        PS: consider using the async client
        if time becomes an issue
        """
        logger.info("Adding documents to vector store")
        for batch_start_index in tqdm(
            range(0, len(documents_to_add), batch_size),
            desc=f"Adding documents to qdrant by batches of {batch_size}",
        ):
            await self.upsert_points(
                points=[
                    PointStruct(
                        id=document_to_add[PARQUET_CHUNK_ID_COLUMN],
                        vector=document_to_add[PARQUET_EMBEDDING_COLUMN],
                        payload=document_to_add[list(metadata_keys)].to_dict(),
                    )
                    for _, document_to_add in documents_to_add[
                        batch_start_index : batch_start_index + batch_size
                    ].iterrows()
                ]
            )

    @backoff.on_exception(
        backoff.constant,
        exception=UnexpectedResponse,
        interval=5,
        max_tries=20,
    )
    async def upsert_points(self, points: list[PointStruct]) -> None:
        """Upsert points to the collection."""
        await self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    @observe(name="retrieve documents")  # type: ignore
    async def similarity_search(
        self,
        query: str,
        k: int,
        embedding_model: Embeddings,
    ) -> list[SearchResult]:
        """Return documents most similar to query."""
        embedding = await embedding_model.aembed_query(query)

        results = await self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            with_payload=True,
            limit=k,
        )

        return [
            SearchResult(id=str(result.id), score=result.score, payload=result.payload)
            for result in results
        ]


class LocalAsyncQdrantVectorStore(AsyncQdrantVectorStore):
    """Wrapper around QdrantClient to index chunks and query them."""

    def __init__(
        self,
        project_environment_variables: ProjectSettings,
    ):
        """Initialize LocalAsyncQdrantVectorStore."""
        self.client = AsyncQdrantClient(
            path=str(project_environment_variables.vector_store_output_folder_path),
            prefer_grpc=False,
        )
        self.collection_name = (
            project_environment_variables.vector_store_collection_name
        )


class RemoteAsyncQdrantVectorStore(AsyncQdrantVectorStore):
    """Wrapper around QdrantClient to index chunks and query them."""

    def __init__(
        self,
        project_environment_variables: ProjectSettings,
    ):
        """Initialize RemoteAsyncQdrantVectorStore."""
        if (
            project_environment_variables.vector_store_url is None
            or project_environment_variables.vector_store_api_key is None
        ):
            raise ValueError(
                "Qdrant remote URL or Qdrant API key are not set in the environment variables"
            )
        self.client = AsyncQdrantClient(
            url=project_environment_variables.vector_store_url,
            api_key=project_environment_variables.vector_store_api_key,
            prefer_grpc=False,
        )
        self.collection_name = (
            project_environment_variables.vector_store_collection_name
        )
