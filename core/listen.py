import time
import threading
from twython import Twython
from twython import TwythonStreamer
from data import database
import pymongo
from core import process


# ---
# Module for streaming Twitter data and adjusting definitions with feedback
# ---


# Initialize Twitter API object with necessary tokens & keys
APP_KEY = "66W0JAKaiGjLdyuf9vIVSysEe"
APP_SECRET = "8diGCspCU2UUjnpzbDqbxnD3c4Yc50Hu7XHzIjGSdF7HDRiCXr"
TOKEN = "856006422-RjbHJ7x0CMyWPEelGQiedyT2JecOo0mJBskan068"
TOKEN_SECRET = "xrLuD2xZVwVChXLr5VWLRBL10Ad6Urow7ks8SW16n7ewt"

twitter = Twython(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)


# Class to stream data of specific Twitter account
class StreamOthers(TwythonStreamer):
    t0 = time.time()

    # Save data upon retrieval
    def on_success(self, data):
        # TODO: save incoming data
        print(data["text"])

        # Change subject of stream every 5 minutes
        if time.time() - StreamOthers.t0 >= 300:
            StreamOthers.t0 = time.time()
            start_other()

    # Disconnect stream on error
    def on_error(self, status_code, data):
        print(status_code)
        self.disconnect()


# Class to stream data of application Twitter account
class StreamMe(TwythonStreamer):

    # On retrieval, check for feedback
    def on_success(self, data):

        # Check if Tweet is in response to previous Tweet by application and if it contains text
        if "in_reply_to_status_id_str" in data and "text" in data:
            tweet_id = data["in_reply_to_status_id_str"]
            tweet = database.sent.find_one({"id_str": str(tweet_id)})
            if tweet is not None:

                # Check if it is positive or negative feedback
                if process.is_positive_feedback(data["text"]):

                    # Save the feedback
                    # Increase score for every definition used in Tweet that the feedback is for
                    # Score increase is relative to the amount of definitions for that stem
                    database.received.save({"id_str": data["id_str"],
                                            "in_reply_to_status_id_str": data["in_reply_to_status_id_str"],
                                            "text": data["text"],
                                            "feedback": 1})
                    for definition_id in tweet["definitions"]:
                        definition = database.definitions.find_one({"_id": definition_id})
                        amount = database.definitions.find({"stem": definition["stem"]}).count()
                        if 1 - definition["score"] > 0:
                            database.definitions.update({"_id": definition_id},
                                                        {"$inc": {"score": (1 - definition["score"]) / amount}})
                else:

                    # Save the feedback
                    # Decrease score for every definition found in feedback
                    # Score decrease is relative to the amount of definitions for that stem
                    database.received.save({"id_str": data["id_str"],
                                            "in_reply_to_status_id_str": data["in_reply_to_status_id_str"],
                                            "text": data["text"],
                                            "feedback": -1})
                    keywords = process.dismantle(data)
                    for definition_id in tweet["definitions"]:
                        definition = database.definitions.find_one({"_id": definition_id})
                        if any(keyword in definition["text"] for keyword in keywords.keys()):
                            amount = database.definitions.find({"stem": definition["stem"]}).count()
                            if 1 - definition["score"] > 0:
                                database.definitions.update({"_id": definition_id},
                                                            {"$inc": {"score": -((1 - definition["score"]) / amount)}})

    # Disconnect stream on error
    def on_error(self, status_code, data):
        print(status_code)
        self.disconnect()


# Create stream objects with necessary tokens & keys
streamOthers = StreamOthers(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)
streamMe = StreamMe(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)


# Start streaming account with highest priority
def start_other():
    cursor = database.accounts.find().sort([("priority", pymongo.ASCENDING)])
    target = next(cursor)
    if target is not None:

        # Update account, increase priority by 1
        print("Listening for: " + target["screenname"] + ", with priority: " + str(target["priority"]))
        database.accounts.update({"screenname": target["screenname"]},
                                 {"screenname": target["screenname"], "priority": target["priority"] + 1})
        streamOthers.statuses.filter(track=target["screenname"])


# Start streaming application account
def start_me():
    streamMe.user()


# Create and start new thread for streaming specific account
def listen_others():
    thread = threading.Thread(target=start_other)
    thread.start()


# Create and start new thread for streaming application account
def listen_me():
    thread = threading.Thread(target=start_me)
    thread.start()
