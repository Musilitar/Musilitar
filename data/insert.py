from data import database
from core.listen import switch_target


def insert(screenname):
    print("Saving account for listening: " + screenname)
    account = database.accounts.find_one({"screenname": screenname})
    if account is None:
        database.accounts.save({"screenname": screenname, "priority": 1})
