"""Chainlit app for the RAGator graph."""
import chainlit as cl

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from langfuse.callback import CallbackHandler

from src.graphs.ragator.config import config as ragator_config
from src.graphs.ragator.graph import graph as ragator_graph


@cl.on_message
async def on_message(msg: cl.Message):
    """Handle incoming messages."""
    # Check if the message is empty
    if not msg.content:
        return

    langchain_handler = cl.LangchainCallbackHandler()
    langfuse_handler = CallbackHandler()

    final_answer = cl.Message(content="")

    async for output in ragator_graph.astream(
        {
            "messages": [HumanMessage(content=msg.content)],
        },
        stream_mode="values",
        config=RunnableConfig(
            **{
                "configurable": {
                    "thread_id": cl.context.session.id,
                    **ragator_config,
                },
                "callbacks": [langchain_handler, langfuse_handler],
            },
        ),
    ):
        state = output["messages"][-1]
        if isinstance(state, HumanMessage):
            continue
        await final_answer.stream_token(state.content)
