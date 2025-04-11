from paths import WORKFLOW_SCHEMAS_FOLDER_PATH
from src.workflow.load_rag_workflow_from_schema import load_rag_workflow_from_schema


def main():
    rag_workflow = load_rag_workflow_from_schema(WORKFLOW_SCHEMAS_FOLDER_PATH / "simple_schema.yaml")

    print(rag_workflow.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()
