from typing import List

from pydantic import BaseModel


class SimpleState(BaseModel):
    message_history: list[str]
    user_metadata: dict[str, str]
    answer:  str | None
    documents: List[str]
