from data.tweets import tweetA, tweetB
from difflib import SequenceMatcher


def dismantle(tweet):
    words = tweet["text"].split()
    return words


def prepareForSimilarity(tweetA, tweetB):
    wordsA = dismantle(tweetA)
    wordsB = dismantle(tweetB)
    items = {
        tweetA["id_str"]: wordsA,
        tweetB["id_str"]: wordsB
    }
    return items


def process():
    score = SequenceMatcher(None, tweetA["text"].lower(), tweetB["text"].lower()).ratio()
    print(score)


process()