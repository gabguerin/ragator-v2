from pydantic import BaseModel


class ChatModelParams(BaseModel):
    """This class is used to define the chat model."""

    module: str
    class_name: str
    model_name: str


class LLMInstructionParams(BaseModel):
    """
    This class is used to define the instruction for the LLM.
    """

    model: ChatModelParams
    system_prompt: str
    human_prompt: str


class EmbeddingParams(BaseModel):
    """This class is used to define the embedding model."""

    module: str
    class_name: str
    model_name: str
    dimension: int


class VectorStoreParams(BaseModel):
    """This class is used to define the vector store."""

    module: str
    class_name: str
    collection_name: str
    retrieve_top_k: int


class RagParams(BaseModel):
    """
    This class is used to define the parameters for the RAG.
    """

    embedding: EmbeddingParams
    vector_store: VectorStoreParams
    llm_instructions: dict[str, LLMInstructionParams]
