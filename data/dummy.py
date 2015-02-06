from data import database

received_tweets = [
    {
        "id_str": "1",
        "text": "An apple can be green red or yellow"
    },
    {
        "id_str": "2",
        "text": "Apples are usually red or green and sometimes yellow"
    },
    {
        "id_str": "3",
        "text": "A pear is green"
    },
    {
        "id_str": "4",
        "text": "What do an apple and a pear have in common?"
    },
    {
        "id_str": "6",
        "text": "What is an apple?"
    },
    {
        "id_str": "8",
        "text": "Apples and pears are types of fruit"
    },
    {
        "id_str": "9",
        "text": "Common means usual or shared equally?"
    },
    {
        "id_str": "10",
        "in_reply_to_status_id_str": "5",
        "text": "Thank you!"
    },
    {
        "id_str": "11",
        "text": "What is a tree?"
    }
]

sent_tweets = [
    {
        "id_str": "5",
        "text": "A type of fruit",
        "definitions": ["0", "1"]
    },
    {
        "id_str": "7",
        "text": "Usual, shared equally"
    },
]

definitions = [
    {
        "stem": "appl",
        "text": "A type of fruit",
        "score": 0.5
    },
    {
        "stem": "pear",
        "text": "A type of fruit",
        "score": 0.5
    },
    {
        "stem": "common",
        "text": "Usual, shared equally",
        "score": 0.5
    },
]

accounts = [
    {
        "screenname": "football",
        "priority": 1
    },
    {
        "screenname": "katy",
        "priority": 1
    }
]


def load():
    database.sent.insert(sent_tweets)
    database.received.insert(received_tweets)
    database.accounts.insert(accounts)
    database.definitions.insert(definitions)
