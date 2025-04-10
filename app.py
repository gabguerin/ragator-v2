from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import HumanMessage

import chainlit as cl
from langgraph.constants import END
from rag_graphs.load_rag_workflow_from_schema import load_rag_workflow_from_schema


@cl.on_message
async def on_message(msg: cl.Message):
    # Prepare LangGraph configuration
    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()

    # Create the message that will be streamed
    final_answer = cl.Message(content="")

    # Load your LangGraph workflow from schema
    rag_workflow = load_rag_workflow_from_schema("rag_graphs/rag_graph_schemas/_base_schema.yaml")

    # Run workflow and stream tokens from the final output
    async for output, metadata in rag_workflow.astream(
        {"messages": [HumanMessage(content=msg.content)]},
        config=RunnableConfig(callbacks=[cb], **config),
        stream_mode="messages"
    ):
        # Only stream the final message when reaching END
        if (
            output.content
            and not isinstance(output, HumanMessage)
            and metadata.get("langgraph_node") == END
        ):
            await final_answer.stream_token(output.content)

    # Send the final streamed message
    await final_answer.send()
