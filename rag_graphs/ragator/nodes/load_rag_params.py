import yaml

from rag_graphs.ragator.models import RagParams, RagState


def main(state: RagState) -> RagState:
    """Load RAG parameters from a YAML file."""
    with open(state.rag_params_path, "r") as f:
        rag_params = RagParams(**yaml.safe_load(f))

    state.rag_params = rag_params
    return state
