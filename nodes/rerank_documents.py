
def main(**kwargs):
    docs = kwargs.get("documents", [])
    return {"documents": sorted(docs)}  # Dummy sort
