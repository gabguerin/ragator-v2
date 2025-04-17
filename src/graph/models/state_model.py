from pydantic import BaseModel


class State(BaseModel):
    id: str
    module_path: str
    class_name: str
