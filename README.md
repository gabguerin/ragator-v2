# ragator-v2

## Overview

Ragator is a tool for generating and managing RAG (Retrieval-Augmented Generation) pipelines. It provides a simple interface to create, configure, evaluate and run RAG pipelines using various backends and models.

## Setup

- To install all the dependencies [install uv](https://docs.astral.sh/uv/getting-started/installation/). 

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
│   ├── utils
│   └── params.py           # Parameters for the LangGraph state
```

