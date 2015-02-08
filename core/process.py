from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import re
import math
from collections import Counter
from data import database


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def tokenize(text):
    lower = text.lower()
    punctuationless = "".join(l for l in lower if l not in string.punctuation)
    tokens = word_tokenize(punctuationless)
    return tokens


def remove_stopwords(tokens):
    filtered = [w for w in tokens if w not in stopwords.words("english")]
    return filtered


def stem(tokens):
    stemmed = {}
    stemmer = PorterStemmer()
    for token in tokens:
        stemmed[stemmer.stem(token)] = 1
    return stemmed


def dismantle(tweet):
    tokenized = tokenize(tweet["text"])
    filtered = remove_stopwords(tokenized)
    stemmed = stem(filtered)
    return stemmed


def is_question(text):
    if "?" in text:
        return True
    return False


def is_positive_feedback(text):
    keywords = [
        "thank",
        "great",
        "super",
        "nice",
        "awesome",
        "cool",
        "fantastic",
        "thanks",
    ]
    if any(keyword in text for keyword in keywords):
        return True
    else:
        return False


def remove_key(dictionary, key):
    temp = dict(dictionary)
    del temp[key]
    return temp


def process(tweet):
    keywords = dismantle(tweet)
    if is_question(tweet["text"]):
        highest_cosine = 0
        questions = database.questions.find()
        for question in questions:
            cosine = get_cosine(dismantle(tweet), dismantle(question))
            if cosine > highest_cosine:
                highest_cosine = cosine
        if highest_cosine < 0.8:
            print("Saving question: " + tweet["text"])
            database.questions.save({"text": tweet["text"]})

        definitions = database.definitions.find({"stem": {"$in": list(keywords.keys())}})
        if definitions is None or definitions.count() == 0:
            return {"keywords": list(keywords.keys())}
        else:
            return {"definitions": definitions}
    else:
        for key in keywords.keys():
            matches = database.definitions.find({key: {"$exists": True}})
            for other in remove_key(keywords, key):
                if other not in matches:
                    print("Saving definition: " + key + " = " + other)
                    database.definitions.save({key: other})
        return None