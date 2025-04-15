import random


def main(**kwargs):
    return {
        "question_classification": random.choice(["OFF_TOPIC", "ON_TOPIC"])
    }
