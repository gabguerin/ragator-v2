import yaml
from pydantic import BaseModel

from src.graph_config import EmbeddingConfig, VectorStoreConfig, ChatModelConfig


class ConfigSchema(BaseModel):
    embedding: EmbeddingConfig
    vector_store: VectorStoreConfig

    classification_chat_model: ChatModelConfig
    rag_chat_model: ChatModelConfig
    question_about_rag_chat_model: ChatModelConfig
    question_out_of_scope_chat_model: ChatModelConfig


with open("data/configs/ragator.yaml") as f:
    config = ConfigSchema(**yaml.safe_load(f)).dict()
