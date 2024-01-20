
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from os import environ

uri = environ.get('MONGO_URI')

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

