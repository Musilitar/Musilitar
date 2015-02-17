from core import process
from data import database, dummy


# ---
# Module for testing the process module
# ---


# Drop the database and load the dummy data
def setup_module(module):
    print("Setup module: %s" % module.__name__)
    database.client.drop_database("musilitar")
    dummy.load()


# Test if "What is an apple?" when processed returns a list of definitions or keywords
def test_question_returns_options():
    print("Testing if question Tweet returns options")
    options = process.process(dummy.received_tweets[4])
    assert "keywords" in options or "definitions" in options
