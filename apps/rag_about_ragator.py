"""
Module: Mermaid Workflow Drawer
Generates and prints a Mermaid diagram from a workflow schema.
"""
from pathlib import Path

from src.graph.compile_rag_graph import compile_rag_graph


def main() -> None:
    """
    Main function to load a workflow schema and draw it as a Mermaid diagram.
    """
    rag_workflow = compile_rag_graph(
        Path("rag_graphs/ragator/rag_graph.yaml")
    )

    print(rag_workflow.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()
