import operator
from typing import Literal

import yaml
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage

import chainlit as cl

from rag_graphs.ragator.nodes.question_out_of_scope import main as question_out_of_scope
from rag_graphs.ragator.nodes.classify_question import main as classify_question
from rag_graphs.ragator.nodes.retrieve_documents import main as retrieve_documents
from rag_graphs.ragator.nodes.generate_llm_answer import main as generate_llm_answer
from rag_graphs.ragator.paths import RAG_PARAMS_PATH
from rag_graphs.ragator.routers.question_classification import main as question_classification


from rag_graphs.ragator.params import RagState, RagParams

builder = StateGraph(RagState)

# Add nodes
builder.add_node("classify_question", classify_question)
builder.add_node("question_out_of_scope", question_out_of_scope)
builder.add_node("retrieve_documents", retrieve_documents)
builder.add_node("generate_llm_answer", generate_llm_answer)

# Add edges
builder.add_edge(START, "classify_question")

# Add conditional routing from classify_question
builder.add_conditional_edges(
    "classify_question",
    question_classification,
    {
        "RAGATOR": "retrieve_documents",
        "RAG": "generate_llm_answer",
        "OTHER": "question_out_of_scope",
    }
)

builder.add_edge("question_out_of_scope", END)
builder.add_edge("retrieve_documents", "generate_llm_answer")
builder.add_edge("generate_llm_answer", END)

# Compile the graph
graph = builder.compile()

with open(RAG_PARAMS_PATH, "r") as f:
    rag_params = yaml.safe_load(f)


@cl.on_message
async def on_message(msg: cl.Message):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()
    final_answer = cl.Message(content="")

    initial_state = {
        "messages": [HumanMessage(content=msg.content)],
        "rag_params": rag_params,
        "question_classification": None,
        "retrieved_chunks": [],
    }
    # Initial RagState
    async for output in graph.astream(initial_state, stream_mode="values",
                                      config=RunnableConfig(callbacks=[cb], **config)):
        state = output["messages"][-1]
        if isinstance(state, HumanMessage):
            continue
        await final_answer.stream_token(state.content)
