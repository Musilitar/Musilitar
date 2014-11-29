from flask import Flask, jsonify
from pymongo import Connection
from api.crossdomain import crossdomain

app = Flask(__name__)
connection = Connection("localhost", 27017)
db = connection.tweets
collection = db.user

@app.route("/t", methods=["GET"])
@crossdomain(origin="*")
def index():
    tweets = []
    for tweet in collection.find():
        tweets.append(tweet)
    return jsonify(text=tweets[0]["text"])

if __name__ == "__main__":
    app.run(debug=True)
