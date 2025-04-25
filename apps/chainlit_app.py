# app.py
import chainlit as cl

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from src.graphs.ragator.config import load_config
from src.graphs.ragator.graph import graph


@cl.on_message
async def on_message(msg: cl.Message):
    config = {
        "configurable": {
            "thread_id": cl.context.session.id,
            **load_config("data/configs/ragator.yaml")
        }
    }
    cb = cl.LangchainCallbackHandler()
    final_answer = cl.Message(content="")

    async for output in graph.astream(
        {
            "messages": [HumanMessage(content=msg.content)],
        },
        stream_mode="values",
        config=RunnableConfig(**config, callbacks=[cb]),
    ):
        state = output["messages"][-1]
        if isinstance(state, HumanMessage):
            continue
        await final_answer.stream_token(state.content)
