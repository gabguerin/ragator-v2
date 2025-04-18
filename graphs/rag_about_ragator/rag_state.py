from typing import List

from pydantic import BaseModel


class RagState(BaseModel):
    user_metadata: dict[str, str]
    message_history: list[str]
    question_classification: str | None
    documents: List[str]
    answer: str | None
