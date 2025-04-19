"""
Module: Mermaid Workflow Drawer
Generates and prints a Mermaid diagram from a workflow schema.
"""
import re
from typing import Annotated

import typer

from src.graph.compile_rag_graph import compile_rag_graph

from pathlib import Path


def update_readme_with_diagram(mermaid_diagram: str, rag_name: str):
    start_tag = f"<!-- {rag_name.upper()}_DIAGRAM_START -->"
    end_tag = f"<!-- {rag_name.upper()}_DIAGRAM_END -->"

    readme_path = Path("README.md")
    readme_text = readme_path.read_text()

    if start_tag not in readme_text or end_tag not in readme_text:
        # If the tags are not found, add them to the README
        readme_text += f"\n{start_tag}\n```mermaid\n{mermaid_diagram}\n```\n{end_tag}"
        readme_path.write_text(readme_text)
        return

    # If the tags are found, replace the old diagram with the new one
    new_block = f"{start_tag}\n```mermaid\n{mermaid_diagram}\n```\n{end_tag}\n"

    pattern = re.compile(f"{start_tag}.*?{end_tag}", re.DOTALL)
    updated_text = pattern.sub(new_block, readme_text)

    readme_path.write_text(updated_text)


def main(
    rag_name: Annotated[str, typer.Option(..., help="Name of the RAG workflow")],
) -> None:
    """
    Main function to load a workflow schema and draw it as a Mermaid diagram.
    """
    rag_workflow = compile_rag_graph(
        rag_graph_schema_yaml_path=Path(f"rag_graphs/{rag_name}/rag_graph_schema.yaml")
    )

    # Generate the Mermaid diagram
    mermaid_diagram = rag_workflow.get_graph().draw_mermaid()

    # Print the Mermaid diagram
    print(mermaid_diagram)

    # Save the Mermaid diagram to README.md
    update_readme_with_diagram(mermaid_diagram, rag_name=rag_name)


if __name__ == "__main__":
    typer.run(main)
