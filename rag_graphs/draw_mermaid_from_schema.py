from rag_graphs.load_rag_workflow_from_schema import load_rag_workflow_from_schema


def main():
    rag_workflow = load_rag_workflow_from_schema("rag_graphs/rag_graph_schemas/_base_schema.yaml")

    print(rag_workflow.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()
