from flask import Flask, render_template, request
from data.insert import insert
from core.process import process
from core.respond import respond
from api import statistics

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    data = statistics.get_all_statistics()
    return render_template("index.html", **data)



@app.route("/insert", methods=["GET", "POST"])
def insert():
    if request.method == "POST":
        insert(request.form["screenname"])
    return render_template("insert.html")


@app.route("/speak", methods=["GET", "POST"])
def speak():
    if request.method == "GET":
        return render_template("ask.html")
    else:
        if "question" in request.form:
            question = {"text": request.form["question"]}
            possibilities = process(question)
            data = {}
            answer = respond(possibilities)
            if answer != "":
                data["response"] = answer
            return render_template("response.html", **data)
        else:
            if "good" in request.form:
                print("Answer was good")
            if "bad" in request.form:
                print("Answer was bad")
            return render_template("ask.html")
