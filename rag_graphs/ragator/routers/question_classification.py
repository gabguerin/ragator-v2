from rag_graphs.ragator.params import RagState


def main(state: RagState) -> str:
    """Route based on the classification result in the state."""
    classification = state.get("question_classification", "").strip().upper()
    if classification in {"RAGATOR", "RAG", "OTHER"}:
        return classification
    return "OTHER"
