from pydantic import BaseModel


class ChatModelConfig(BaseModel):
    """This class is used to define the chat model."""

    module: str
    class_name: str
    model_name: str
    system_prompt: str
    human_prompt: str


class EmbeddingConfig(BaseModel):
    """This class is used to define the embedding model."""

    module: str
    class_name: str
    model_name: str
    dimension: int


class VectorStoreConfig(BaseModel):
    """This class is used to define the vector store."""

    module: str
    class_name: str
    collection_name: str
    retrieve_top_k: int
