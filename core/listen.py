import time
import threading
from twython import Twython
from twython import TwythonStreamer
from data import database, dummy
import pymongo


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
            switch_target()

    def on_error(self, status_code, data):
        print(status_code)
        self.disconnect()


class StreamMe(TwythonStreamer):
    def on_success(self, data):
        if "in_reply_to_status_id_str" in data:
            original_id = data["in_reply_to_status_id_str"]
            original_tweet = database.sent.find_one({"id_str": original_id})
            if original_tweet is not None:
                definitions = database.definitions.find({"definitions.in": original_id})
                if definitions is not None:
                    print("ullo1")
                    for definition in definitions:
                        print("ullo2")
                        amount = len(definition["definitions"])
                        # database.definitions.update({"stem": definition["stem"]},{"$inc": {"score": 1}})

    def on_error(self, status_code, data):
        print(status_code)
        self.disconnect()

streamOthers = StreamOthers(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)
streamMe = StreamMe(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)


def switch_target():
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


def listen_others():
    thread = threading.Thread(target=switch_target)
    thread.start()


def listen_me():
    streamMe.on_success(dummy.received_tweets[7])
