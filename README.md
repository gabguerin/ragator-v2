# ragator-v2

## Overview

Ragator is a tool for generating and managing RAG (Retrieval-Augmented Generation) pipelines. It provides a simple interface to create, configure, evaluate and run RAG pipelines using various backends and models.

## Setup

- [Install uv](https://docs.astral.sh/uv/getting-started/installation/) to manage your Python versions, virtual environments, dependencies and tooling configs. 

- [Create a virtual environment with uv](https://docs.astral.sh/uv/pip/environments/#creating-a-virtual-environment) for the project.

- Install the project dependencies in the new venv:

    ```bash
    uv install
    ```

## Code structure

```markdown
.
├── ...
├── src/
│   ├── generation/
│   │   ├── chat_models/    # Wrappers for chat completion models
│   │   └── embeddings/     # Wrappers for embedding models
│   ├── retrieval/
│   │   ├── file_handlers/  # File handlers for different file types
│   │   └── vector_stores/  # Wrappers for vector databases
│   ├── graphs/
│   │   ├── your_graph/
│   │   │   ├── nodes/      # State modifier functions
│   │   │   ├── state.py    # State definition
│   │   │   ├── graph.py    # Graph definition in LangGraph
│   │   │   └── params.py   # Parameters for the graph
│   │   └── ...
│   ├── utils/              # Utility functions
│   └── params.py           # Parameters for the LangGraph state
```

## Graphs
### ragator graph

<!-- RAGATOR_DIAGRAM_START -->
```mermaid
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	classify_question(classify_question)
	generate_llm_response_from_context(generate_llm_response_from_context)
	retrieve_context(retrieve_context)
	generate_llm_response(generate_llm_response)
	__end__([<p>__end__</p>]):::last
	__start__ --> classify_question;
	generate_llm_response --> __end__;
	generate_llm_response_from_context --> __end__;
	retrieve_context --> generate_llm_response_from_context;
	classify_question -. &nbsp;RAGATOR&nbsp; .-> retrieve_context;
	classify_question -. &nbsp;RAG&nbsp; .-> generate_llm_response;
	classify_question -. &nbsp;OUT_OF_SCOPE&nbsp; .-> generate_llm_response;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc

```
<!-- RAGATOR_DIAGRAM_END -->