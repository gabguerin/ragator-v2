# app.py
import chainlit as cl
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from rag_graphs.ragator.params import RagState
from src.graph.create_rag_graph import create_rag_graph

# Initialize the graph once (or per session if needed)
graph = create_rag_graph("rag_graphs/ragator/rag_graph_schema.yaml").compile()


@cl.on_message
async def on_message(msg: cl.Message):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()
    final_answer = cl.Message(content="")

    initial_state = RagState(
        rag_params=None,
        messages=[HumanMessage(content=msg.content)],
        retrieved_chunks=[],
        question_classification=None,
    )

    for msg, metadata in graph.stream(
            initial_state,
            stream_mode="messages",
            config=RunnableConfig(callbacks=[cb], **config)
    ):
        if (
                msg.content
                and not isinstance(msg, HumanMessage)
                and metadata["langgraph_node"] == "final"
        ):
            await final_answer.stream_token(msg.content)

    await final_answer.send()
