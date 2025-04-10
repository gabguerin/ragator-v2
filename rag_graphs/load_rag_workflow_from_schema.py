import yaml
from langgraph.constants import END
from langgraph.graph import StateGraph

from rag_graphs.rag_graph_model import RagGraphSchema
from utils.importlib import import_module_from_path


def load_rag_workflow_from_schema(yaml_path: str):
    with open(yaml_path, "r") as f:
        config = yaml.safe_load(f)

    rag_graph_schema = RagGraphSchema(**config)

    state_type = import_module_from_path(
        module_path=rag_graph_schema.state_type.module_path,
        object_name=rag_graph_schema.state_type.class_name,
    )
    workflow = StateGraph(state_type)

    # Add nodes
    for node in rag_graph_schema.nodes:
        function = import_module_from_path(node.module_path, node.function_name)
        workflow.add_node(node.id, function)

    # Add entry point
    workflow.set_entry_point(rag_graph_schema.entry_point)

    # Add edges
    for edge in rag_graph_schema.edges:
        if "condition" in edge.model_fields:
            edge_function = import_module_from_path(edge.condition.module_path, edge.condition.function_name)
            mapping = {
                from_condition: (END if to_node == "__end__" else to_node)
                for from_condition, to_node in edge.mapping.items()
            }
            workflow.add_conditional_edges(edge.from_node, edge_function, mapping)
        else:
            workflow.add_edge(edge.from_node, edge.to_node)

    return workflow.compile()
