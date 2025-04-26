from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from src.graphs.ragator.config import ConfigSchema
from src.graphs.ragator.nodes.classify_question import classify_question
from src.graphs.ragator.nodes.generate_llm_response import generate_llm_response
from src.graphs.ragator.nodes.generate_llm_response_from_context import (
    generate_llm_response_from_context,
)
from src.graphs.ragator.nodes.retrieve_context import retrieve_context
from src.graphs.ragator.state import StateSchema


graph_builder = StateGraph(StateSchema, ConfigSchema)

# Add nodes
graph_builder.add_node("classify_question", classify_question)
graph_builder.add_node(
    "generate_llm_response_from_context", generate_llm_response_from_context
)
graph_builder.add_node("retrieve_context", retrieve_context)
graph_builder.add_node("generate_llm_response", generate_llm_response)

# Add edges
graph_builder.add_edge(START, "classify_question")

# Add conditional routing from classify_question
graph_builder.add_conditional_edges(
    "classify_question",
    # Routing based on classification
    lambda state: state.question_classification,
    {
        "RAGATOR": "retrieve_context",
        "RAG": "generate_llm_response",
        "OUT_OF_SCOPE": "generate_llm_response",
    },
)

graph_builder.add_edge("generate_llm_response", END)
graph_builder.add_edge("retrieve_context", "generate_llm_response_from_context")
graph_builder.add_edge("generate_llm_response_from_context", END)

# Compile the graph
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
