"""This module defines the data models for a workflow schema using Pydantic."""
from typing import List

from pydantic import BaseModel


class Node(BaseModel):
    """
    A class representing a node in a workflow.

    Attributes:
        id (str): The unique identifier of the node.
        module_path (str): The path to the module that defines the node.
        function_name (str): The name of the function associated with the node.
    """

    id: str
    module_path: str
    function_name: str


class ConditionalEdge(BaseModel):
    """
    A class representing a conditional edge in a workflow.
    Attributes:
        from_node (str): The ID of the node from which the edge originates.
        condition (Node): The condition node that determines the next node.
        mapping (dict[str, str]): Key: the output of the node 'from_node', Value: the id of the next node
    """

    from_node: str
    condition: Node
    mapping: dict[str, str]


class Edge(BaseModel):
    """
    A class representing a simple edge in a workflow.
    """

    from_node: str
    to_node: str


class State(BaseModel):
    """
    A class representing the state of a workflow.
    Attributes:
        id (str): The unique identifier of the state.
        module_path (str): The path to the module that defines the state.
        class_name (str): The name of the class associated with the state.
    """

    id: str
    module_path: str
    class_name: str


class RagGraphSchema(BaseModel):
    """
    A class representing a workflow schema.
    Attributes:
        state (State): The state of the workflow.
        entry_point (str): The entry point of the workflow.
        nodes (List[Node]): A list of nodes in the workflow.
        edges (List[Edge | ConditionalEdge]): A list of edges in the workflow.
    """

    state: State
    entry_point: str
    nodes: List[Node]
    edges: List[Edge | ConditionalEdge]
