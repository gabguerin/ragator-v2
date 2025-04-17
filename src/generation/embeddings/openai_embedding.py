from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

EMBEDDING_MODEL_NAME = "text-embedding-3-small"

openai_embedding_model = OpenAIEmbeddings(
    model=EMBEDDING_MODEL_NAME,
)
