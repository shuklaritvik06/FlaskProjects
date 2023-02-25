import os

from pymongo import MongoClient

USER_NAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")


def get_database():
    CONNECTION_STRING = f"mongodb+srv://{USER_NAME}:{PASSWORD}@cluster0.aeiaykn.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    return client['students']


db = get_database()
collection_cse = db["cse"]
collection_bme = db["bme"]
collection_ece = db["ece"]
