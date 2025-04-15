import os
import tempfile
import shutil
from typing import List

from git import Repo
from langchain_core.documents import Document

from retrieval.files.python_file import PythonFile


async def main(github_url: str) -> List[Document]:
    temp_dir = tempfile.mkdtemp()

    try:
        print(f"Cloning {github_url} into {temp_dir}")
        Repo.clone_from(github_url, temp_dir)

        documents = []
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    py_file = PythonFile(file_path)
                    docs = await py_file.to_documents()
                    documents.extend(docs)

        return documents

    finally:
        shutil.rmtree(temp_dir)
