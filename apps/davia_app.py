from davia import Davia, run_server

from src.graphs.ragator.config import config
from src.graphs.ragator.graph import graph_builder

davia_app = Davia()


@davia_app.graph
def ragator_graph():
    """
    A minimal LangGraph agent that returns a greeting.
    """
    return graph_builder, config


#  Launch the server
if __name__ == "__main__":
    run_server(davia_app)
