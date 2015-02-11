from core import process, respond
from data import database, dummy
from models import definition


def setup_module(module):
    print("Setup module: %s" % module.__name__)
    database.client.drop_database("musilitar")
    dummy.load()


def test_created_aggregate():
    result = process.process(dummy.received_tweets[9])
    answer = respond.respond(result)
    assert definition.are_aggregates(answer)


def test_used_aggregate():
    result = process.process(dummy.received_tweets[9])
    answer = respond.respond(result)
    assert definition.are_aggregates(answer)


def test_created_aggregate_when_match():
    result = process.process(dummy.received_tweets[3])
    answer = respond.respond(result)
    assert definition.are_aggregates(answer)