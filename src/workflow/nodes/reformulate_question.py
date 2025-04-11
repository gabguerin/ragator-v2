
def main(**kwargs):
    question = kwargs.get("question", "")
    # Dummy reformulation
    return {"question": question.strip().capitalize()}
