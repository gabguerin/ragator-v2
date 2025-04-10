from typing import List, Dict
from pydantic import BaseModel


class NodeConfig(BaseModel):
    id: str
    module_path: str
    function_name: str


class ConditionalEdge(BaseModel):
    from_node: str
    condition: NodeConfig
    mapping: Dict[str, str]     # Key: the output of the node 'from_node', Value: the id of the next node


class Edge(BaseModel):
    from_node: str
    to_node: str


class StateType(BaseModel):
    id: str
    module_path: str
    class_name: str


class RagGraphSchema(BaseModel):
    state_type: StateType
    entry_point: str
    nodes: List[NodeConfig]
    edges: List[Edge | ConditionalEdge]
