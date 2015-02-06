import math
from core import search
from data import database


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def respond(definitions):
    answer = ""
    if definitions is None or len(definitions) == 0:
        search.search(["tree"])
    else:
        length = len(definitions)
        for definitionA in definitions:
            matches = 0
            for definitionB in definitions:
                if definitionA["text"] == definitionB["text"]:
                    matches += 1
                    if matches > length / 2:
                        answer = definitionA
                        # TODO: save with id_str from returned Twitter status update object
                        database.answers.save({"text": definitionA["text"], "definitions": [definitionA["_id"]]})
    return answer