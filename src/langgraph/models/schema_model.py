from typing import List
from pydantic import BaseModel

from src.langgraph.models.edge_model import Edge, ConditionalEdge
from src.langgraph.models.node_model import Node
from src.langgraph.models.state_model import State


class Schema(BaseModel):
    state: State
    entry_point: str
    nodes: List[Node]
    edges: List[Edge | ConditionalEdge]
