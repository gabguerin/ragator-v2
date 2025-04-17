from langchain.schema.runnable.config import RunnableConfig

import chainlit as cl
from graph.constants import END

from paths import WORKFLOW_SCHEMAS_FOLDER_PATH
from src.graph.utils.load_rag_workflow_from_schema import load_rag_workflow_from_schema
from langgraph_rags.rag_about_ragator.rag_state import RagState


@cl.on_start
async def on_start():
    """Initialize session state when a new user session starts."""
    cl.user_session["message_history"] = []
    cl.user_session["user_metadata"] = {}  # Optional: prefill if needed
    await cl.Message(content="Welcome! Ask me anything to get started.").send()


@cl.on_message
async def on_message(msg: cl.Message):
    thread_id = cl.context.session.id
    cb = cl.LangchainCallbackHandler()
    final_answer = cl.Message(content="")

    # Append the current user message to message history
    cl.user_session["message_history"].append(f"User: {msg.content}")

    # Load the LangGraph RAG workflow
    rag_workflow = load_rag_workflow_from_schema(
        WORKFLOW_SCHEMAS_FOLDER_PATH / "auchan_schema.yaml"
    )

    # Build input for SimpleState
    initial_state = RagState(
        message_history=cl.user_session["message_history"],
        user_metadata={},  # Fill if you're collecting metadata
        question_classification=None,
        answer=None,
        documents=[],
    )

    # Run graph and stream output
    async for output, metadata in rag_workflow.astream(
        initial_state,
        config=RunnableConfig(callbacks=[cb], configurable={"thread_id": thread_id}),
        stream_mode="messages",
    ):
        if metadata.get("langgraph_node") == END:
            final_answer_text = output.get("answer")
            if final_answer_text:
                await final_answer.stream_token(final_answer_text)
                # Store assistant's reply in message history
                cl.user_session["message_history"].append(
                    f"Assistant: {final_answer_text}"
                )

    await final_answer.send()
