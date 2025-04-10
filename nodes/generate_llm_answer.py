
def main(**kwargs):
    docs = kwargs.get("documents", [])
    return {"answer": f"LLM-generated answer using: {docs}"}
