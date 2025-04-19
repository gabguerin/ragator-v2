import yaml

from rag_graphs.ragator.params import RagParams, RagState
from rag_graphs.ragator.paths import RAG_PARAMS_PATH


def main(state: RagState):
    """Load RAG parameters from a YAML file."""
    with open(RAG_PARAMS_PATH, "r") as f:
        rag_params = RagParams(**yaml.safe_load(f))

    return {"rag_params": rag_params}
