# app.py
import chainlit as cl
import yaml
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.constants import END

from rag_graphs.ragator.params import RagState, RagParams
from rag_graphs.ragator.paths import RAG_PARAMS_PATH, RAG_GRAPH_SCHEMA_PATH
from src.graph.create_rag_graph import create_rag_graph

# Initialize the graph once (or per session if needed)
graph = create_rag_graph(RAG_GRAPH_SCHEMA_PATH).compile()


@cl.on_chat_start
async def on_chat_start() -> None:
    """Called when the chat starts."""
    try:
        with open(RAG_PARAMS_PATH, "r") as f:
            rag_params = RagParams(**yaml.safe_load(f))
    except Exception as e:
        raise RuntimeError(f"Failed to load RAG params: {e}")

    cl.user_session.set("rag_params", rag_params)


@cl.on_message
async def on_message(msg: cl.Message):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()
    final_answer = cl.Message(content="")

    # Initial RagState
    initial_state = RagState(
        rag_params=cl.user_session.get("rag_params"),
        messages=[HumanMessage(content=msg.content)],
        question_classification=None,
        retrieved_chunks=[],
    )

    for state_update, metadata in graph.stream(
        input=initial_state,
        stream_mode="messages",
        config=RunnableConfig(callbacks=[cb], **config),
    ):
        print(f"State Update: {state_update}, Metadata: {metadata}")
        if metadata["langgraph_node"] == END:
            last_msg = state_update.messages[-1]
            await final_answer.stream_token(last_msg.content)

    await final_answer.send()
