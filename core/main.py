from data import dummy
from data import database
from core import process, respond
from api import api


def main():
    database.client.drop_database("musilitar")
    dummy.load()
    result = process.process(dummy.received_tweets[8])
    answer = respond.respond(result)
    print(answer)
    api.app.run()


if __name__ == "__main__":
    main()
