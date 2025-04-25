# ragator-v2

## Overview

Ragator is a tool for generating and managing RAG (Retrieval-Augmented Generation) pipelines. It provides a simple interface to create, configure, evaluate and run RAG pipelines using various backends and models.

## Setup

- [Install uv](https://docs.astral.sh/uv/getting-started/installation/) to manage your Python versions, virtual environments, dependencies and tooling configs. 

- [Create a virtual environment with uv](https://docs.astral.sh/uv/pip/environments/#creating-a-virtual-environment) for the project.

- Install the project dependencies in the new venv:

    ```bash
    uv sync	--all-extras --dev
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
│   │   ├── <name-of-your-rag>/
│   │   │   ├── nodes/      # State modifier functions
│   │   │   ├── state.py    # State definition
│   │   │   ├── graph.py    # Graph definition in LangGraph
│   │   │   └── config.py   # Configuration for the graph
│   │   └── ...
│   ├── utils/              # Utility functions
│   └── graph_config.py     # TypedDicts to define the configuration of the graphs
```

## RAG Configuration & Parametrization

### State definition
The state is defined in `src/graphs/<name-of-your-rag>/state.py`. 

```python

class StateSchema(TypedDict):
    """State schema of the RAGator."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    # Add other parameters to the state as needed
```
[See state example](src/graphs/ragator/state.py)

### Config definition
The config is defined in `src/graphs/<name-of-your-rag>/config.py`. 

Use the configurations of the EmbeddingConfig, VectorStoreConfig and ChatModelConfig classes define in [src/graph_config.py](src/graph_config.py) to configure your RAG. 

```python

class ConfigSchema(TypedDict):
    """Configuration schema for the RAGator."""
    
    embedding: dict[str, str]                   # Embedding model config
    vector_store: dict[str, str]                # Vector store config
    <node_using_a_chat_model>: dict[str, str]   # Chat model config
```
[See config example](src/graphs/ragator/config.py)

### Node implementation

Implement different nodes in the `src/graphs/<name-of-your-rag>/nodes/` directory. 

Each node should be a Python function that takes the *state as input* and returns a dict with the modified parameters of the state.

```python
def <node_name>(state: StateSchema, config: ConfigSchema) -> dict:
    # Use the state and config to access the messages and rag parameters
    # message_history = state["messages"]
    # 
    # embedding_config = EmbeddingConfig(**config["configurable"]["embedding"])
    # vector_store_config = VectorStoreConfig(**config["configurable"]["vector_store"])
    # chat_model_config = ChatModelConfig(**config["configurable"]["<node_using_a_chat_model>"])
    # 
    # ...
    return {"parameter_of_state": modified_parameter_of_state}
```
[See node example](src/graphs/ragator/nodes/classify_question.py)

### Graph definition
The graph is defined in `src/graphs/<name-of-your-rag>/graph.py`.

```python
# Define the state used in the graph
graph_builder = StateGraph(StateSchema, ConfigSchema)

# Add nodes
graph_builder.add_node("your_node", <node_name>)

# Add edges
graph_builder.add_edge(START, "your_node")
graph_builder.add_edge("your_node", END)

# Compile the graph
graph = graph_builder.compile()
```
[See graph example](src/graphs/ragator/graph.py)

### RAG parametrization

This parameters will be loaded if needed in your nodes. 
The yaml file is located in `src/graphs/<name-of-your-rag>/params.yaml` and has the same structure as RagParams. 

```yaml
embedding:
  module: <path.to.embedding.module>
  class_name: <EmbeddingModelClass>
  model_name: <embedding-model-name>
  dimension: <embedding-dimension>

vector_store:
  module: <path.to.vector.store.module>
  class_name: <VectorStoreClass>
  collection_name: <name-of-your-collection>
  retrieve_top_k: <number-of-top-results>

<node_using_chat_model>:
  module: <path.to.chat.model.module>
  class_name: <ChatModelClass>
  model_name: <llm-model-name>
  
  system_prompt: |
    <System prompt tailored to the task>

  human_prompt: |
    <Human prompt template using {question}, {context}, or {message_history}>

```
[See params example](data/configs/ragator.yaml)

## RAG examples

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
