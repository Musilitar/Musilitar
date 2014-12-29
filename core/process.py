from data.tweets import tweetA, tweetB
from difflib import SequenceMatcher
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import re, math
from collections import Counter


WORD = re.compile(r'\w+')


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


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


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


def process():
    # score = SequenceMatcher(None, tweetA["text"].lower(), tweetB["text"].lower()).ratio()
    cosine = get_cosine(dismantle(tweetA), dismantle(tweetB))
    print(cosine)


process()