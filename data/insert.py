from data import database
from core.listen import start_listening


def insert(screenname):
    print("Saving account for listening: " + screenname)
    database.accounts.save({"screenname": screenname})
    start_listening(screenname)
