from twython import Twython
from data import database

# Initialize Twitter API object with necessary tokens & keys for main account, Musilitar
APP_KEY_MUSILITAR = "66W0JAKaiGjLdyuf9vIVSysEe"
APP_SECRET_MUSILITAR = "8diGCspCU2UUjnpzbDqbxnD3c4Yc50Hu7XHzIjGSdF7HDRiCXr"
TOKEN_MUSILITAR = "856006422-RjbHJ7x0CMyWPEelGQiedyT2JecOo0mJBskan068"
TOKEN_SECRET_MUSILITAR = "xrLuD2xZVwVChXLr5VWLRBL10Ad6Urow7ks8SW16n7ewt"
twitter_musilitar = Twython(APP_KEY_MUSILITAR, APP_SECRET_MUSILITAR, TOKEN_MUSILITAR, TOKEN_SECRET_MUSILITAR)

# Initialize Twitter API object with necessary tokens & keys for test account, Ratilisum
APP_KEY_RATILISUM = "jlXD4WuL2jZ7NCpI6UooIhR8M"
APP_SECRET_RATILISUM = "yzW7w3OfKIjmXsoGDCj68FLOEcjOSE71Ybka3XVzXJoPR8xH5G"
TOKEN_RATILISUM = "2899892488-lugB1DCGaZRlRpKgNZHz7TwSKnE44yRyhUnM2vv"
TOKEN_SECRET_RATILISUM = "HH624tbZBgndk90UhZvmbqqdO84dcBWzuzriUVcSTV2YB"
twitter_ratilisum = Twython(APP_KEY_RATILISUM, APP_SECRET_RATILISUM, TOKEN_RATILISUM, TOKEN_SECRET_RATILISUM)


# Return correct Twitter API object for given account
def get_twitter_for_account(account):
    if account == "musilitar":
        return twitter_musilitar
    if account == "ratilisum":
        return twitter_ratilisum


# Tweet given status using given account
def tweet_status(text, account="musilitar"):
    twitter = get_twitter_for_account(account)
    twitter.update_status(status=text)


# Tweet a response using given list of answers, Tweet to respond to and specified account
def tweet_response(answer, tweet, account="musilitar"):
    twitter = get_twitter_for_account(account)
    id_str = tweet["in_reply_to_status_id_str"]
    screen_name = "@" + tweet["user"]["screen_name"]
    text = "".join(definition["text"] for definition in answer)
    status = screen_name + " " + text

    response = twitter.update_status(status=status, in_reply_to_status_id_str=id_str)
    database.sent.save(response)
