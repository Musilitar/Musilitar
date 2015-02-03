from data import database

tweets = [
    {
        "id_str": 1,
        "text": "An apple can be green red or yellow"
    },
    {
        "id_str": 2,
        "text": "Apples are usually red or green and sometimes yellow"
    },
    {
        "id_str": 3,
        "text": "A pear is green"
    },
    {
        "id_str": 4,
        "text": "What do an apple and a pear have in common?"
    },
    {
        "id_str": 5,
        "text": "A type of fruit"
    }
]

definitions = [
    {
        "appl": "A type of fruit"
    },
    {
        "pear": "A type of fruit"
    },
    {
        "common": "Usual, shared equally"
    }
]


def load():
    for tweet in tweets:
        database.tweets.insert(tweet)
    for definition in definitions:
        database.definitions.insert(definition)
