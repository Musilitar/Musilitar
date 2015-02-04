from pymongo import MongoClient

client = MongoClient()
db = client.musilitar
tweets = db.tweets
questions = db.questions
answers = db.answers
definitions = db.definitions
accounts = db.accounts
