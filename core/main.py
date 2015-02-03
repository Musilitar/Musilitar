from twython import Twython
from twython import TwythonStreamer
from data import dummy
from data import database
from core.process import process
from core.respond import respond

APP_KEY = "66W0JAKaiGjLdyuf9vIVSysEe"
APP_SECRET = "8diGCspCU2UUjnpzbDqbxnD3c4Yc50Hu7XHzIjGSdF7HDRiCXr"
TOKEN = "856006422-RjbHJ7x0CMyWPEelGQiedyT2JecOo0mJBskan068"
TOKEN_SECRET = "xrLuD2xZVwVChXLr5VWLRBL10Ad6Urow7ks8SW16n7ewt"

twitter = Twython(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)


class Streamer(TwythonStreamer):
    def on_success(self, data):
        if "text" in data:
            if data["user"]["screen_name"] != "Musilitar":
                # id_str = data["id_str"]
                # response = "@" + data["user"]["screen_name"] + " " + dismantle(data)
                # twitter.update_status(status=response, in_reply_to_status_id_str=id_str)
                print(data["text"].encode("utf-8"))

    def on_error(self, status_code, data):
        print(status_code)
        self.disconnect()


def main():
    # tweet = twitter.get_home_timeline()[0]
    # tweets.insert(tweet)
    database.client.drop_database("musilitar")
    dummy.load()
    listen()


def listen():
    # streamer = Streamer(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)
    # streamer.user()
    possibilities = process(dummy.tweets[3])
    answer = respond(possibilities)
    print(answer)


if __name__ == "__main__":
    main()
