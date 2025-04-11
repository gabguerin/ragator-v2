"""Vector store utilities."""

from abc import ABC, abstractmethod

import pandas as pd
from langchain.embeddings.base import Embeddings

from src.models import SearchResult, SupportedVectorStore
from src.settings import ProjectSettings, project_environment_variables


class AsyncVectorStore(ABC):
    """Vector store interface."""

    @abstractmethod
    async def create_or_overwrite_collection_if_exists(
        self, embedding_size: int
    ) -> None:
        """Create a collection. Overwrite it if it already exists."""
        ...

    @abstractmethod
    async def add_documents_to_vector_store(
        self,
        documents_to_add: pd.DataFrame,
        metadata_keys: tuple[str, ...],
        batch_size: int = 128,
    ) -> None:
        """Add new documents to the vector store."""
        ...

    @abstractmethod
    async def similarity_search(
        self,
        query: str,
        k: int,
        embedding_model: Embeddings,
    ) -> list[SearchResult]:
        """Search for similar documents."""
        ...


def get_async_vector_store(
    project_environment_variables: ProjectSettings = project_environment_variables,
) -> AsyncVectorStore:
    """Get the vector store client."""
    match project_environment_variables.selected_vector_store:
        case SupportedVectorStore.QdrantLocal:
            from src.vector_store.qdrant_vector_store import LocalAsyncQdrantVectorStore

            return LocalAsyncQdrantVectorStore(
                project_environment_variables=project_environment_variables
            )

        case SupportedVectorStore.QdrantRemote:
            from src.vector_store.qdrant_vector_store import (
                RemoteAsyncQdrantVectorStore,
            )

            return RemoteAsyncQdrantVectorStore(
                project_environment_variables=project_environment_variables
            )

        case _:
            raise ValueError("Unsupported vector store")
