import os
from typing import List

from dotenv import load_dotenv
from openai import AsyncOpenAI

from .base import BaseEmbeddingModel

load_dotenv()


class OpenAIEmbeddingModel(BaseEmbeddingModel):
    def initialize_client(self):
        """Initialize the OpenAI client."""
        return AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def embed_query(self, text: str) -> List[float]:
        response = await self.client.embeddings.create(
            model=self.model_name,
            dimensions=self.dimensions,
            input=text,
        )
        return response.data[0].embedding

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        response = await self.client.embeddings.create(
            model=self.model_name,
            dimensions=self.dimensions,
            input=texts,
        )
        return [d.embedding for d in response.data]
