from data import database


# ---
# Module for inserting into the database
# ---


# Save account if it's not already in the database
def insert(screenname):
    print("Saving account for listening: " + screenname)
    account = database.accounts.find_one({"screenname": screenname})
    if account is None:
        database.accounts.save({"screenname": screenname, "priority": 1})
