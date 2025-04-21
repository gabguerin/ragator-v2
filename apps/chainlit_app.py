# app.py
from pathlib import Path

import chainlit as cl
import yaml
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from rag_graphs.ragator.graph import graph


RAGATOR_PARAMS_PATH = Path("rag_graphs/ragator/params.yaml")


@cl.on_chat_start
async def on_chat_start() -> None:
    """Called when the chat starts."""
    try:
        with open(RAGATOR_PARAMS_PATH, "r") as f:
            rag_params = yaml.safe_load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load RAG params: {e}")

    cl.user_session.set("rag_params", rag_params)


@cl.on_message
async def on_message(msg: cl.Message):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()
    final_answer = cl.Message(content="")

    initial_state = {
        "messages": [HumanMessage(content=msg.content)],
        "rag_params": cl.user_session.get("rag_params"),
        "question_classification": None,
        "retrieved_chunks": [],
    }
    # Initial RagState
    async for output in graph.astream(
        initial_state,
        stream_mode="values",
        config=RunnableConfig(callbacks=[cb], **config),
    ):
        state = output["messages"][-1]
        if isinstance(state, HumanMessage):
            continue
        await final_answer.stream_token(state.content)
