from pymongo import Connection
from twython import Twython
from twython import TwythonStreamer

APP_KEY = "66W0JAKaiGjLdyuf9vIVSysEe"
APP_SECRET = "8diGCspCU2UUjnpzbDqbxnD3c4Yc50Hu7XHzIjGSdF7HDRiCXr"
TOKEN = "856006422-RjbHJ7x0CMyWPEelGQiedyT2JecOo0mJBskan068"
TOKEN_SECRET = "xrLuD2xZVwVChXLr5VWLRBL10Ad6Urow7ks8SW16n7ewt"

twitter = Twython(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)


class Streamer(TwythonStreamer):
    def on_success(self, data):
        if 'id_str' in data:
            id_str = data['id_str']
            text = "@" + data['user']['screen_name'] + " Right back at you!"
            twitter.update_status(status=text, in_reply_to_status_id_str=id_str)
            print(data['text'].encode('utf-8'))

    def on_error(self, status_code, data):
        print(status_code)


def main():
    connection = Connection("localhost", 27017)
    db = connection.tweets
    collection = db.user

    tweet = twitter.get_home_timeline()[0]
    collection.insert(tweet)


def echo():
    streamer = Streamer(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)
    streamer.user()


if __name__ == "__main__":
    main()
