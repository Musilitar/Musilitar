from core import process, respond
from data import database, dummy
from models import definition


# ---
# Module for testing the respond module
# ---


# Drop the database and load the dummy data
def setup_module(module):
    print("Setup module: %s" % module.__name__)
    database.client.drop_database("musilitar")
    dummy.load()


# Test if "What is a pear?" created a new aggregate definition when processed and then used in respond()
# This is when the database only contains the dummy data and should not contain an aggregate for that yet
def test_created_aggregate():
    result = process.process(dummy.received_tweets[9])
    answer = respond.respond(result)
    assert definition.are_aggregates(answer)


# Test if "What is a pear?" used an existing aggregate definition when processed and then used in respond()
# This is after the previous test, so it should find an existing one
def test_used_aggregate():
    result = process.process(dummy.received_tweets[9])
    answer = respond.respond(result)
    assert definition.are_aggregates(answer)


# Test if "What do an apple and a pear have in common?" created a new aggregate definition from matches
# This is after the previous tests, so it should match on pear and apple both having "A type of fruit" as definition
def test_created_aggregate_when_match():
    result = process.process(dummy.received_tweets[3])
    answer = respond.respond(result)
    assert definition.are_aggregates(answer)