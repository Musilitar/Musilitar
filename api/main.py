from flask import Flask, jsonify
from pymongo import Connection

app = Flask(__name__)
connection = Connection("localhost", 27017)
db = connection.tweets
collection = db.user

@app.route("/t", methods=["GET"])
def index():
    tweets = []
    for tweet in collection.find():
        tweets.append(tweet)
    return jsonify(text=tweets[0]["text"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
