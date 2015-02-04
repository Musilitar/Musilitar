from flask import Flask, render_template, request
from data.insert import insert

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        insert(request.form["screenname"])
    return render_template("insert.html")


'''@app.route("/t", methods=["GET"])
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
    return jsonify(text=questions[index]["text"])'''


if __name__ == "__main__":
    app.run()
    # app.run(host="0.0.0.0", port=80, debug=True)