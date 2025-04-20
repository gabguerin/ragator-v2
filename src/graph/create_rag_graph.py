"""Module to compile a langgraph RAG from a YAML schema file."""
from pathlib import Path

import yaml
from langgraph.constants import END, START
from langgraph.graph.state import StateGraph

from src.utils.importlib import import_module_from_path
from src.graph.models import Schema


def create_rag_graph(rag_graph_schema_yaml_path: str | Path) -> StateGraph:
    """Load a langgraph rag from a YAML schema file."""
    with open(rag_graph_schema_yaml_path, "r") as f:
        config = yaml.safe_load(f)

    rag_graph_schema = Schema(**config)

    state_class = import_module_from_path(
        module_path=rag_graph_schema.state.module_path,
        object_name=rag_graph_schema.state.class_name,
    )
    rag_graph = StateGraph(type(state_class))

    # Add nodes
    for node in rag_graph_schema.nodes:
        function = import_module_from_path(node.module_path, node.function_name)
        rag_graph.add_node(node.id, function)

    # Add edges
    for edge in rag_graph_schema.edges:
        # Handle special cases for start nodes
        edge.from_node = edge.from_node if edge.from_node != "__start__" else START

        # If the edge is a normal edge, add it directly
        if "to_node" in edge.model_fields:
            edge.to_node = edge.to_node if edge.to_node != "__end__" else END
            rag_graph.add_edge(edge.from_node, edge.to_node)

        # If the edge is a conditional edge, import the router function and add it
        else:
            router = import_module_from_path(
                edge.condition.module_path, edge.condition.function_name
            )
            mapping = {
                from_condition: to_node if to_node != "__end__" else END
                for from_condition, to_node in edge.mapping.items()
            }
            rag_graph.add_conditional_edges(edge.from_node, router, mapping)

    return rag_graph
