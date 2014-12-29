from pymongo import Connection
from twython import Twython
from twython import TwythonStreamer

APP_KEY = "66W0JAKaiGjLdyuf9vIVSysEe"
APP_SECRET = "8diGCspCU2UUjnpzbDqbxnD3c4Yc50Hu7XHzIjGSdF7HDRiCXr"
TOKEN = "856006422-RjbHJ7x0CMyWPEelGQiedyT2JecOo0mJBskan068"
TOKEN_SECRET = "xrLuD2xZVwVChXLr5VWLRBL10Ad6Urow7ks8SW16n7ewt"

twitter = Twython(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)
connection = Connection("localhost", 27017)
tweets = connection.tweets
tUser = tweets.user
tAQuestions = tweets.aquestions
tUQuestions = tweets.uquestions
tKInfo = tweets.kinfo
tUInfo = tweets.uinfo


class Streamer(TwythonStreamer):
    def on_success(self, data):
        if "text" in data:
            if data["user"]["screen_name"] != "Musilitar":
                #id_str = data["id_str"]
                #response = "@" + data["user"]["screen_name"] + " " + dismantle(data)
                #twitter.update_status(status=response, in_reply_to_status_id_str=id_str)
                print(data["text"].encode("utf-8"))

    def on_error(self, status_code, data):
        print(status_code)
        self.disconnect()


def main():
    # tweet = twitter.get_home_timeline()[0]
    # tweets.insert(tweet)
    listen()


def listen():
    streamer = Streamer(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)
    streamer.user()


def dismantle(tweet):
    inAnswered = tAQuestions.find_one({"text": tweet["text"]})
    inUnanswered = tUQuestions.find_one({"text": tweet["text"]})
    inKnown = tKInfo.find_one({"text": tweet["text"]})
    inUnknown = tUInfo.find_one({"text": tweet["text"]})
    if "?" in tweet["text"]:
        if inAnswered is None and inUnanswered is None:
            tUQuestions.insert(tweet)
            return "Question, new"
        elif inAnswered is not None:
            return "Question, answered"
        else:
            return "Question, unanswered"
    else:
        if inKnown is None and inUnknown is None:
            tUInfo.insert(tweet)
            return "Info, new"
        elif inKnown is not None:
            return "Info, known"
        else:
            return "Info, unknown"


if __name__ == "__main__":
    main()
