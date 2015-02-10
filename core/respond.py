import math
from core import search
from data import database
from models import definition as definition_model


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


def respond(result):
    answer = []
    if "keywords" in result:
        answer = search.search(result["keywords"])
    else:
        definitions = result["definitions"]
        length = len(definitions)
        match_exists = False
        for definitionA in definitions:
            matches = 0
            for definitionB in definitions:
                if definitionA["text"] == definitionB["text"]:
                    matches += 1
            if matches >= length / 2:
                match_exists = True
                answer.append(definitionA)
                # TODO: save with id_str from returned Twitter status update object
                database.answers.save({"text": definitionA["text"], "definitions": [definitionA["_id"]]})

        if not match_exists:
            text = ""
            ids = []
            new_definitions = []
            used_stems = []

            for i, definition in enumerate(definitions):
                if i > 0:
                    text += "; " + definition["text"]
                else:
                    text += definition["text"]
                ids.append(definition["_id"])

            for definition in definitions:
                if definition["stem"] not in used_stems:
                    used_stems.append(definition["stem"])
                    highest_scoring_aggregate = definition_model.get_highest_scoring_aggregate(definition["stem"])
                    if highest_scoring_aggregate is not None:
                        other_ids = list(ids)
                        other_ids.remove(highest_scoring_aggregate["_id"])
                        if all(definition_id in highest_scoring_aggregate["using"] for definition_id in other_ids):
                            print("Using existing aggregate definition")
                            answer.append(highest_scoring_aggregate)
                    else:
                        new_definition = {"stem": definition["stem"], "text": text, "score": 0.5, "using": ids}
                        new_definitions.append(new_definition)
                        print("Saving new definition: " + str(new_definition))
                        database.definitions.save(new_definition)

            if len(answer) == 0:
                answer = new_definitions
    print("Produced answer: " + str(answer))
    return answer