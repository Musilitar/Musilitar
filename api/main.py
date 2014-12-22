from flask import Flask, jsonify
from pymongo import Connection

app = Flask(__name__)
connection = Connection("localhost", 27017)
tweets = connection.tweets
tUser = tweets.user
tAQuestions = tweets.aquestions
tUQuestions = tweets.uquestions
tKInfo = tweets.kinfo
tUInfo = tweets.uinfo


@app.route("/", methods=["GET"])
def home():
    return "I am Musilitar. I am too big for the box."


@app.route("/t", methods=["GET"])
def tweets():
    tweets = []
    for tweet in tUser.find():
        tweets.append(tweet)
    return jsonify(text=tweets[0]["text"])


@app.route("/uq", methods=["GET"])
def unansweredMostRecent():
    questions = []
    for question in tUQuestions.find():
        questions.append(question)
    return jsonify(text=questions[0]["text"])

@app.route("/uq/<int:index>", methods=["GET"])
def unansweredByID(index):
    questions = []
    for question in tUQuestions.find():
        questions.append(question)
    return jsonify(text=questions[index]["text"])


if __name__ == "__main__":
    app.run()
    #app.run(host="0.0.0.0", port=80, debug=True)
