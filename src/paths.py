"""
Module: Paths Configuration
Defines paths for workflow schemas and LLM instruction files used in the project.
"""

from pathlib import Path

WORKFLOW_SCHEMAS_FOLDER_PATH: Path = Path("data/rags/rag_about_ragator/rag_workflows")
LLM_INSTRUCTIONS_FOLDER_PATH: Path = Path("data/rags/rag_about_ragator/llm_instructions")
INPUT_FILES: Path = Path("data/documents/rag_about_ragator/input_files")
