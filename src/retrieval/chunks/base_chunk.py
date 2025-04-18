from typing import Optional

from pydantic import BaseModel, Field


class Chunk(BaseModel):
    content: str = Field(default_factory=str)
    source: str = Field(default_factory=str)
    uuid: str = Field(default_factory=str)

    score: Optional[float] = Field(default=None)
    embedding: Optional[list[float]] = Field(default=None)
