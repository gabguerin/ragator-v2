import random


def main(**kwargs):
    return {
        "question_classification": random.choice(["QUESTION_DE_GAMME", "QUESTION_ORIGINE_ET_SANTE", "AUTRE"])
    }
