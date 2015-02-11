from data import database


def get_amount_definitions():
    amount = database.definitions.find().count()
    return amount


def get_amount_sent_tweets():
    amount = database.sent.find().count()
    return amount


def get_amount_received_tweets():
    amount = database.received.find().count()
    return amount


def get_percentage_positive_feedback():
    result = database.received.find({"feedback": {"$exists": True}})
    feedback = list(result)
    amount_feedback = len(list(feedback))
    positive = [tweet for tweet in feedback if tweet["feedback"] == 1]
    amount_positive = len(positive)
    if amount_positive > 0:
        percentage = 100 / (amount_feedback / amount_positive)
    else:
        percentage = 0
    return percentage


def get_stem_with_most_definitions():
    stem = database.definitions.aggregate([{"$group": {"_id": "$stem", "amount": {"$sum": 1}}},
                                           {"$sort": {"amount": -1}},
                                           {"$limit": 1}])
    if stem is not None:
        if len(stem["result"]) > 0:
            return stem["result"][0]["_id"] + " (" + str(stem["result"][0]["amount"]) + ")"
    else:
        return "nothing was found"


def get_amount_accounts():
    amount = database.accounts.find().count()
    return amount


def get_best_definition():
    definition = database.definitions.aggregate([{"$group": {"_id": {"_id": "$stem", "text": "$text"},
                                                             "score": {"$max": "$score"}}},
                                                 {"$sort": {"score": -1}},
                                                 {"$limit": 1}])
    if definition is not None:
        if len(definition["result"]) > 0:
            return definition["result"][0]["_id"]["_id"] + ": " + definition["result"][0]["_id"]["text"] + " (" + str(definition["result"][0]["score"]) + ")"
    else:
        return "nothing was found"


def get_all_statistics():
    data = {
        "amount_definitions": get_amount_definitions(),
        "amount_sent_tweets": get_amount_sent_tweets(),
        "amount_received_tweets": get_amount_received_tweets(),
        "amount_accounts": get_amount_accounts(),
        "percentage_positive_feedback": get_percentage_positive_feedback(),
        "stem_most_definitions": get_stem_with_most_definitions(),
        "best_definition": get_best_definition()
    }
    return data
