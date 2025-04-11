from typing import List
from pydantic import BaseModel

from workflow.models.edge_model import Edge, ConditionalEdge
from workflow.models.node_model import Node
from workflow.models.state_model import State


class Schema(BaseModel):
    state: State
    entry_point: str
    nodes: List[Node]
    edges: List[Edge | ConditionalEdge]
