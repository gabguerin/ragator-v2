from typing import List
from pydantic import BaseModel

from src.graph.models.edge_model import Edge, ConditionalEdge
from src.graph.models.node_model import Node
from src.graph.models.state_model import State


class Schema(BaseModel):
    state: State
    entry_point: str
    nodes: List[Node]
    edges: List[Edge | ConditionalEdge]
