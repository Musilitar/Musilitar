from data import database
import pymongo


# ---
# Module for model of definition, to provide functionality for working with them
# ---


# Return whether definitions are aggregates or not
def are_aggregates(definitions):
    if all("using" in definition for definition in definitions):
        return True
    else:
        return False


# Return the highest scoring aggregate for a stem
def get_highest_scoring_aggregate(stem):
    result = database.definitions.find({"stem": stem, "using": {"$exists": True}}).sort([("score", pymongo.DESCENDING)]).limit(1)
    match = list(result)
    if match is not None and len(match) > 0:
        return match[0]
    else:
        return None


# Return whether a specified string already exists as a definition for a given stem
def text_exists_for_stem(stem, text):
    result = database.definitions.find_one({"stem": stem, "text": text})
    if result is not None:
        return True
    else:
        return False


# Return whether a given definition is the highest scoring one for that stem
def is_highest_scoring(definition):
    matches = database.definitions.find({"stem": definition["stem"]}).sort([("score", pymongo.DESCENDING)])
    if matches is not None and len(list(matches)) > 0:
        if matches[0]["score"] == definition["score"]:
            return True
    else:
        return False
