from typing import List

from pydantic import BaseModel


class BaseStateGraph(BaseModel):
    message_history: list[str]
    answer:  str | None
    documents: List[str]
