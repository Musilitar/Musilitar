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
        used_stems = []
        without_aggregates = [definition for definition in definitions if "using" not in definition]
        for definition in without_aggregates:
            matches = 0
            other_definitions = list(without_aggregates)
            other_definitions.remove(definition)
            for other in other_definitions:
                if definition["text"] == other["text"]:
                    matches += 1
            if matches > 0:
                used_stems.append(definition["stem"])
                # TODO: save with id_str from returned Twitter status update object
                # database.answers.save({"text": definitionA["text"], "definitions": [definitionA["_id"]]})

        if len(used_stems) > 0:
            text = ""
            ids = []
            usable_definitions = [definition for definition in definitions if definition["stem"] in used_stems and "using" not in definition]
            for i, definition in enumerate(usable_definitions):
                if definition["text"] not in text:
                    if i > 0:
                        text += "; " + definition["text"]
                    else:
                        text += definition["text"]
                ids.append(definition["_id"])

            for stem in used_stems:
                if not definition_model.text_exists_for_stem(stem, text):
                    new_definition = {"stem": stem, "text": text, "score": 0.5, "using": ids}
                    answer.append(new_definition)
                    print("Saving new definition: " + str(new_definition))
                    database.definitions.save(new_definition)

        else:
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