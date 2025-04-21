from langgraph.constants import START, END
from langgraph.graph import StateGraph

from rag_graphs.ragator.nodes.classify_question import main as classify_question
from rag_graphs.ragator.nodes.question_out_of_scope import main as question_out_of_scope
from rag_graphs.ragator.nodes.retrieve_documents import main as retrieve_documents
from rag_graphs.ragator.nodes.generate_llm_answer import main as generate_llm_answer
from rag_graphs.ragator.routers.question_classification import (
    main as question_classification,
)

from rag_graphs.ragator.params import RagState


graph_builder = StateGraph(RagState)

# Add nodes
graph_builder.add_node("classify_question", classify_question)
graph_builder.add_node("question_out_of_scope", question_out_of_scope)
graph_builder.add_node("retrieve_documents", retrieve_documents)
graph_builder.add_node("generate_llm_answer", generate_llm_answer)

# Add edges
graph_builder.add_edge(START, "classify_question")

# Add conditional routing from classify_question
graph_builder.add_conditional_edges(
    "classify_question",
    question_classification,
    {
        "RAGATOR": "retrieve_documents",
        "RAG": "generate_llm_answer",
        "OTHER": "question_out_of_scope",
    },
)

graph_builder.add_edge("question_out_of_scope", END)
graph_builder.add_edge("retrieve_documents", "generate_llm_answer")
graph_builder.add_edge("generate_llm_answer", END)

# Compile the graph
graph = graph_builder.compile()
