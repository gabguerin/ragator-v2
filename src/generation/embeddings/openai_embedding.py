
from langchain_openai import OpenAIEmbeddings

EMBEDDING_MODEL_NAME = "text-embedding-3-small"

openai_embedding_model = OpenAIEmbeddings(
    model=EMBEDDING_MODEL_NAME,
)
