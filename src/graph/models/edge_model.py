from typing import Dict
from pydantic import BaseModel

from src.graph.models.node_model import Node


class ConditionalEdge(BaseModel):
    from_node: str
    condition: Node
    mapping: Dict[
        str, str
    ]  # Key: the output of the node 'from_node', Value: the id of the next node


class Edge(BaseModel):
    from_node: str
    to_node: str
