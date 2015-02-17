from pymongo import MongoClient


# ---
# Module for keeping global database variables
# ---


# Main connection
client = MongoClient()

# Main database
db = client.musilitar

# Collections
tweets = db.tweets
sent = tweets.sent
received = tweets.received
questions = db.questions
answers = db.answers
definitions = db.definitions
accounts = db.accounts
