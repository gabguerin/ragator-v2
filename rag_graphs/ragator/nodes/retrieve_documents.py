from typing import Any

from langchain_core.embeddings import Embeddings

from rag_graphs.ragator.params import RagState, EmbeddingParams, VectorStoreParams
from src.retrieval.vector_stores.base_store import BaseVectorStore
from src.utils.importlib import import_module_from_path


def main(state: RagState) -> dict:
    """Retrieve documents using a language model and a retriever."""
    embedding_params: EmbeddingParams = state.rag_params.embedding
    vector_store_params: VectorStoreParams = state.rag_params.vector_store

    # Load embedding model
    embedding_model_class: Any = import_module_from_path(
        module_path=embedding_params.module, object_name=embedding_params.class_name
    )
    embedding_model: Embeddings = embedding_model_class(
        model=embedding_params.model_name,
        dimensions=embedding_params.dimension,
    )

    # Create vector store
    vector_store_class: Any = import_module_from_path(
        module_path=vector_store_params.module,
        object_name=vector_store_params.class_name,
    )
    vector_store: BaseVectorStore = vector_store_class(embedding_model=embedding_model)

    retrieved_chunks = vector_store.similarity_search(
        collection_name=vector_store_params.collection_name,
        query=state.messages[-1].content,
        k=15,
    )

    return {"retrieved_chunks": retrieved_chunks}
