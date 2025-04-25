from typing import Any

from langchain_core.runnables import RunnableConfig

from src.generation.embeddings.base import BaseEmbeddingModel
from src.graphs.ragator.state import StateSchema
from src.graph_config import VectorStoreConfig, EmbeddingConfig
from src.retrieval.vector_stores.base import BaseVectorStore
from src.utils.importlib import import_module_from_path


async def retrieve_context(state: StateSchema, config: RunnableConfig) -> dict:
    """Retrieve documents using a language model and a retriever."""

    embedding_params = EmbeddingConfig(**config["configurable"]["embedding"])
    vector_store_params = VectorStoreConfig(
        **config["configurable"]["vector_store"]
    )

    # Load embedding model
    embedding_model_class: Any = import_module_from_path(
        module_path=embedding_params.module, object_name=embedding_params.class_name
    )
    embedding_model: BaseEmbeddingModel = embedding_model_class(
        model_name=embedding_params.model_name,
        dimensions=embedding_params.dimension,
    )

    # Create vector store
    vector_store_class: Any = import_module_from_path(
        module_path=vector_store_params.module,
        object_name=vector_store_params.class_name,
    )
    vector_store: BaseVectorStore = vector_store_class(embedding_model=embedding_model)

    retrieved_chunks = await vector_store.similarity_search(
        collection_name=vector_store_params.collection_name,
        query=state["messages"][-1].content,
        k=vector_store_params.retrieve_top_k,
    )

    return {"retrieved_chunks": retrieved_chunks}
