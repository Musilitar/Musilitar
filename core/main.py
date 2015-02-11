from data import dummy
from data import database
from core import process, respond
from api import api, statistics


def main():
    database.client.drop_database("musilitar")
    dummy.load()
    api.app.run()


if __name__ == "__main__":
    main()
