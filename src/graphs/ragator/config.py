from typing import TypedDict

import yaml

from src.graph_config import EmbeddingConfig, VectorStoreConfig, ChatModelConfig


class ConfigSchema(TypedDict):
    embedding: dict[str, str]
    vector_store: dict[str, str]

    classification_chat_model: dict[str, str]
    rag_chat_model: dict[str, str]
    question_about_rag_chat_model: dict[str, str]
    question_out_of_scope_chat_model: dict[str, str]


def load_config(config_file_path: str) -> dict[str, dict[str, str]]:
    """Load the config file."""
    with open(config_file_path) as f:
        config = ConfigSchema(**yaml.safe_load(f))

    # Embedding model
    embedding_config = EmbeddingConfig(**config["embedding"])

    # Vector store
    vector_store_config = VectorStoreConfig(**config["vector_store"])

    # Chat models
    classification_chat_model_config = ChatModelConfig(
        **config["classification_chat_model"]
    )
    rag_chat_model_config = ChatModelConfig(**config["rag_chat_model"])
    question_about_rag_chat_model_config = ChatModelConfig(
        **config["question_about_rag_chat_model"]
    )
    question_out_of_scope_chat_model_config = ChatModelConfig(
        **config["question_out_of_scope_chat_model"]
    )

    return {
        # Embedding model
        "embedding": embedding_config.dict(),
        # Vector store
        "vector_store": vector_store_config.dict(),
        # Chat models
        "classification_chat_model": classification_chat_model_config.dict(),
        "rag_chat_model": rag_chat_model_config.dict(),
        "question_about_rag_chat_model": question_about_rag_chat_model_config.dict(),
        "question_out_of_scope_chat_model": question_out_of_scope_chat_model_config.dict(),
        "classification_chat_model_params": classification_chat_model_config.dict(),
    }
