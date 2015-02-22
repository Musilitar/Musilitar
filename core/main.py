from data import dummy
from data import database
from core import process, respond, listen, tweeter
from api import api, statistics


# ---
# Module for main application loop
# ---


# Drop database, load dummy data, start web server
def main():
    database.client.drop_database("musilitar")
    dummy.load()
    listen.listen_me()


if __name__ == "__main__":
    main()
