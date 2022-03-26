import os

from dotenv import load_dotenv
from mongoengine import connect, Document, StringField, IntField

load_dotenv()

USERNAME = os.getenv("MONGODB_USERNAME")
PASSWORD = os.getenv("MONGODB_PASSWORD")
URL = os.getenv("MONGOATLAS_URL")


connect('tkinvt', host=f"mongodb+srv://{USERNAME}:{PASSWORD}@{URL}?retryWrites=true&w=majority")


class TwitterUser(Document):
    twitter_id = IntField()
    name = StringField()

    def __repr__(self):
        return f"{self.name}"
