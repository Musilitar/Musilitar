import time
import threading
from twython import Twython
from twython import TwythonStreamer
from data import database
import pymongo
from core import process


APP_KEY = "66W0JAKaiGjLdyuf9vIVSysEe"
APP_SECRET = "8diGCspCU2UUjnpzbDqbxnD3c4Yc50Hu7XHzIjGSdF7HDRiCXr"
TOKEN = "856006422-RjbHJ7x0CMyWPEelGQiedyT2JecOo0mJBskan068"
TOKEN_SECRET = "xrLuD2xZVwVChXLr5VWLRBL10Ad6Urow7ks8SW16n7ewt"

twitter = Twython(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)


class StreamOthers(TwythonStreamer):
    t0 = time.time()

    def on_success(self, data):
        # TODO: save incoming data
        print(data["text"])
        if time.time() - StreamOthers.t0 >= 300:
            StreamOthers.t0 = time.time()
            start_other()

    def on_error(self, status_code, data):
        print(status_code)
        self.disconnect()


class StreamMe(TwythonStreamer):
    def on_success(self, data):
        if "in_reply_to_status_id_str" in data and "text" in data:
            tweet_id = data["in_reply_to_status_id_str"]
            tweet = database.sent.find_one({"id_str": str(tweet_id)})
            if tweet is not None:
                if process.is_positive_feedback(data["text"]):
                    for definition_id in tweet["definitions"]:
                        definition = database.definitions.find_one({"id": definition_id})
                        amount = database.definitions.find({"stem": definition["stem"]}).count()
                        if 1 - definition["score"] > 0:
                            database.definitions.update({"id": definition_id},
                                                        {"$inc": {"score": (1 - definition["score"]) / amount}})
                else:
                    keywords = process.dismantle(data)
                    for definition_id in tweet["definitions"]:
                        definition = database.definitions.find_one({"id": definition_id})
                        if definition["text"] in keywords.keys():
                            amount = database.definitions.find({"stem": definition["stem"]}).count()
                            if 1 - definition["score"] > 0:
                                database.definitions.update({"id": definition_id},
                                                            {"$inc": {"score": -((1 - definition["score"]) / amount)}})


    def on_error(self, status_code, data):
        print(status_code)
        self.disconnect()

streamOthers = StreamOthers(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)
streamMe = StreamMe(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)


def start_other():
    cursor = database.accounts.find().sort([("priority", pymongo.ASCENDING)])
    target = next(cursor)
    if target is not None:
        print(target)
        print("Listening for: " + target["screenname"] + ", with priority: " + str(target["priority"]))
        database.accounts.update({"screenname": target["screenname"]},
                                 {"screenname": target["screenname"], "priority": target["priority"] + 1})
        updated = database.accounts.find_one({"screenname": target["screenname"]})
        if updated is not None:
            print("Updated " + updated["screenname"] + " to priority " + str(updated["priority"]))
        streamOthers.statuses.filter(track=target["screenname"])


def start_me():
    streamMe.user()


def listen_others():
    thread = threading.Thread(target=start_other)
    thread.start()


def listen_me():
    thread = threading.Thread(target=start_me)
    thread.start()
