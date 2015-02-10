from core import process
from data import database, dummy


def setup_module(module):
    print("Setup module: %s" % module.__name__)
    database.client.drop_database("musilitar")
    dummy.load()


def test_question_returns_options():
    print("Testing if question Tweet returns options")
    options = process.process(dummy.received_tweets[4])
    assert "keywords" in options or "definitions" in options
