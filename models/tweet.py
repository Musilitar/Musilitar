# ---
# Module for model of tweet, to provide functionality for working with them
# ---


# Check if incoming Tweet was not send by application
def is_not_from_me(data):
    if "user" in data:
        if "screen_name" in data["user"]:
            if data["user"]["screen_name"] != "Musilitar":
                return True
    return False


# Check if application was mentioned in incoming Tweet
def is_mentioning_me(data):
    if "entities" in data:
        if "user_mentions" in data["entities"]:
            if any(user_mention["screen_name"] == "Musilitar" for user_mention in data["entities"]["user_mentions"]):
                return True
    return False
