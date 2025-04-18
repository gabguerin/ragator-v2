"""
Module: Paths Configuration
Defines paths for workflow schemas and LLM instruction files used in the project.
"""

from pathlib import Path

# LLMS and embeddings
GENERATION_FOLDER_PATH = Path("src/generation")
LLMS_FOLDER_PATH = GENERATION_FOLDER_PATH / "llms"
EMBEDDINGS_FOLDER_PATH = GENERATION_FOLDER_PATH / "embeddings"

# Document ingestion
RETRIEVAL_FOLDER_PATH = Path("src/retrieval")
FILE_HANDLERS_FOLDER_PATH = RETRIEVAL_FOLDER_PATH / "file_handlers"
VECTOR_STORE_FOLDER_PATH = RETRIEVAL_FOLDER_PATH / "vector_stores"

# Workflow schemas
LANGGRAPH_FOLDER_PATH = Path("src/workflows")
LANGGRAPH_MODELS_FOLDER_PATH = LANGGRAPH_FOLDER_PATH / "models"
LANGGRAPH_UTILS_FOLDER_PATH = LANGGRAPH_FOLDER_PATH / "utils"

# Utility functions
UTILS_FOLDER_PATH = Path("src/utils")
