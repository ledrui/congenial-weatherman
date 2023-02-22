import os
from os import getenv

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from odmantic import AIOEngine

MONGO_USERNAME = getenv("MONGO_USER", default="username")
MONGO_PASSWORD = getenv("MONGO_PASSWORD", default="root")
MONGO_HOST = getenv("MONGO_HOST", default="localhost")
MONGO_PORT = getenv("MONGO_PORT", default="27017")
MONGO_URL = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@mongo:{MONGO_PORT}/"

MONGO_DATABASE = getenv("MONGO_DATABASE", default="test")

# instanciate the mongo client
client = AsyncIOMotorClient(MONGO_URL)
engine = AIOEngine(client=client, database="example_db")

# get database
db = client[MONGO_DATABASE]
