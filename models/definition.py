from data import database
import pymongo


def are_aggregates(definitions):
    if all("using" in definition for definition in definitions):
        return True
    else:
        return False


def get_highest_scoring_aggregate(stem):
    result = database.definitions.find({"stem": stem, "using": {"$exists": True}}).sort([("score", pymongo.DESCENDING)]).limit(1)
    match = list(result)
    if match is not None and len(match) > 0:
        return match[0]
    else:
        return None


def is_highest_scoring(definition):
    matches = database.definitions.find({"stem": definition["stem"]}).sort([("score", pymongo.DESCENDING)])
    if matches is not None and len(list(matches)) > 0:
        if matches[0]["score"] == definition["score"]:
            return True
    else:
        return False
