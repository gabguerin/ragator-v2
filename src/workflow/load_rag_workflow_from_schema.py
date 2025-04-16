import yaml
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from utils.importlib import import_module_from_path
from workflow.models.schema_model import Schema


def load_rag_workflow_from_schema(yaml_path: str) -> "CompiledStateGraph":
    with open(yaml_path, "r") as f:
        config = yaml.safe_load(f)

    workflow_schema = Schema(**config)

    state_class = import_module_from_path(
        module_path=workflow_schema.state.module_path,
        object_name=workflow_schema.state.class_name,
    )
    workflow = StateGraph(type(state_class))

    # Add nodes
    for node in workflow_schema.nodes:
        function = import_module_from_path(node.module_path, node.function_name)
        workflow.add_node(node.id, function)

    # Add entry point
    workflow.set_entry_point(workflow_schema.entry_point)

    # Add edges
    for edge in workflow_schema.edges:
        if "condition" in edge.model_fields:
            edge_function = import_module_from_path(
                edge.condition.module_path, edge.condition.function_name
            )
            mapping = {
                from_condition: (END if to_node == "__end__" else to_node)
                for from_condition, to_node in edge.mapping.items()
            }
            workflow.add_conditional_edges(edge.from_node, edge_function, mapping)
        else:
            workflow.add_edge(edge.from_node, edge.to_node)

    return workflow.compile()
