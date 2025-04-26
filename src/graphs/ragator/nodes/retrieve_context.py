from typing import Any

from langchain_core.runnables import RunnableConfig

from src.generation.embeddings.base import BaseEmbeddingModel
from src.graphs.ragator.config import ConfigSchema
from src.graphs.ragator.state import StateSchema
from src.retrieval.vector_stores.base import BaseVectorStore
from src.utils.importlib import import_module_from_path


async def retrieve_context(state: StateSchema, config: RunnableConfig) -> dict:
    """Retrieve documents using a language model and a retriever."""

    # Load configuration
    config = ConfigSchema(**config["configurable"])

    # Load embedding model
    embedding_model_class: Any = import_module_from_path(
        module_path=config.embedding.module, object_name=config.embedding.class_name
    )
    embedding_model: BaseEmbeddingModel = embedding_model_class(
        model_name=config.embedding.model_name,
        dimensions=config.embedding.dimension,
    )

    # Create vector store
    vector_store_class: Any = import_module_from_path(
        module_path=config.vector_store.module,
        object_name=config.vector_store.class_name,
    )
    vector_store: BaseVectorStore = vector_store_class(embedding_model=embedding_model)

    retrieved_chunks = await vector_store.similarity_search(
        collection_name=config.vector_store.collection_name,
        query=state.messages[-1].content,
        k=config.vector_store.retrieve_top_k,
    )

    return {"retrieved_chunks": retrieved_chunks}
