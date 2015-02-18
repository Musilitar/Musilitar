from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import math
from data import database
import pymongo


# ---
# Module for processing Tweets
# ---


# Return similarity (0 - 1) between to dictionaries
# Copyright:
# StackOverflow user vpekar
# http://stackoverflow.com/questions/15173225/how-to-calculate-cosine-similarity-given-2-sentence-strings-python
# Date of consultation: 29/12/2014
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


# Return tokenized, punctuationless array of words from string
def tokenize(text):
    lower = text.lower()
    punctuationless = "".join(l for l in lower if l not in string.punctuation)
    tokens = word_tokenize(punctuationless)
    return tokens


# Return array of words with stopwords removed
def remove_stopwords(tokens):
    filtered = [w for w in tokens if w not in stopwords.words("english")]
    return filtered


# Return dictionary of stemmed words
def stem(tokens):
    stemmed = {}
    stemmer = PorterStemmer()

    # Set value to 1 for every key
    for token in tokens:
        stemmed[stemmer.stem(token)] = 1
    return stemmed


# Return tokenized, filtered and stemmed dictionary of keywords from Tweet text
def dismantle(tweet):
    tokenized = tokenize(tweet["text"])
    filtered = remove_stopwords(tokenized)
    stemmed = stem(filtered)
    return stemmed


# Return whether a string is a question
def is_question(text):
    if "?" in text:
        return True
    return False


# Return whether a string is positive feedback
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


# Return dictionary with specified key removed
def remove_key(dictionary, key):
    temp = dict(dictionary)
    del temp[key]
    return temp


# Process a Tweet
def process(tweet):

    # Get keywords from Tweet by dismantling it
    keywords = dismantle(tweet)

    # Check if Tweet is a question
    if is_question(tweet["text"]):
        highest_cosine = 0
        questions = database.questions.find()

        # Check if a similar question (> 0.8) is already in database
        for question in questions:
            cosine = get_cosine(dismantle(tweet), dismantle(question))
            if cosine > highest_cosine:
                highest_cosine = cosine
        if highest_cosine < 0.8:

            # If not, save it
            print("Saving question: " + tweet["text"])
            database.questions.save({"text": tweet["text"]})

        # Find definitions related to the question
        definitions = database.definitions.find({"stem": {"$in": list(keywords.keys())}}).sort([("score", pymongo.DESCENDING)])
        if definitions is None or definitions.count() == 0:

            # If no definitions were found, just return the keywords
            return {"keywords": list(keywords.keys())}
        else:
            return {"definitions": list(definitions)}
    else:

        # Find definitions for the keywords in the Tweet
        for key in keywords.keys():
            matches = database.definitions.find({key: {"$exists": True}})
            for other in remove_key(keywords, key):
                if other not in matches:
                    print("Saving definition: " + key + " = " + other)
                    database.definitions.save({key: other})
        return None