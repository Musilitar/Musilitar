from core import process, respond, listen, tweeter
from data import database, dummy
import time


# ---
# Module for testing the listen module
# ---


# Drop the database and start listening for incoming tweets
def setup_module(module):
    print("Setup module: %s" % module.__name__)
    database.client.drop_database("musilitar")
    dummy.load()
    listen.listen_me()