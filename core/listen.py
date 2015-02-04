import time
import threading
from twython import Twython
from twython import TwythonStreamer


APP_KEY = "66W0JAKaiGjLdyuf9vIVSysEe"
APP_SECRET = "8diGCspCU2UUjnpzbDqbxnD3c4Yc50Hu7XHzIjGSdF7HDRiCXr"
TOKEN = "856006422-RjbHJ7x0CMyWPEelGQiedyT2JecOo0mJBskan068"
TOKEN_SECRET = "xrLuD2xZVwVChXLr5VWLRBL10Ad6Urow7ks8SW16n7ewt"

twitter = Twython(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)
pool = ["football", "katy"]


class Streamer(TwythonStreamer):
    def on_success(self, data):
        print(data["text"])

    def on_error(self, status_code, data):
        print(status_code)
        self.disconnect()

    def terminate(self):
        time.sleep(5)
        # listen(pool[1])
        self.disconnect()


def listen(screenname):
    streamer = Streamer(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)
    thread = threading.Thread(target=streamer.terminate)
    thread.start()
    streamer.statuses.filter(track=screenname)


listen("football")
