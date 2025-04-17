"""
Module: Workflow Node Model
Defines the data model for nodes in a workflow.
"""

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
