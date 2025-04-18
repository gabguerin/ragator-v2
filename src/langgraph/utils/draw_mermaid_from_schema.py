"""
Module: Mermaid Workflow Drawer
Generates and prints a Mermaid diagram from a workflow schema.
"""

from paths import WORKFLOW_SCHEMAS_FOLDER_PATH
from src.langgraph.load_rag_workflow_from_schema import load_rag_workflow_from_schema


def main() -> None:
    """
    Main function to load a workflow schema and draw it as a Mermaid diagram.
    """
    rag_workflow = load_rag_workflow_from_schema(
        str(WORKFLOW_SCHEMAS_FOLDER_PATH / "simple_schema.yaml")
    )

    print(rag_workflow.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()
