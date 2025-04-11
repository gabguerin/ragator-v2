import random


def main(**kwargs):
    return random.choice(
        ["QUESTION_DE_GAMME", "QUESTION_ORIGINE_ET_SANTE", "AUTRE"]
    )
