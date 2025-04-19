from davia import Davia, run_server

from src.graph.create_rag_graph import create_rag_graph


davia_app = Davia()


@davia_app.graph
def ragator_graph():
    """
    A minimal LangGraph agent that returns a greeting.
    """
    graph = create_rag_graph("rag_graphs/ragator/rag_graph_schema.yaml")
    return graph


#  Launch the server
if __name__ == "__main__":
    run_server(davia_app)
