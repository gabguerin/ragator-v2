from typing import Optional

from pydantic import BaseModel


class Node(BaseModel):
    id: str
    module_path: str
    function_name: str
