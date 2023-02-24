import os
from dotenv import load_dotenv

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

load_dotenv(".env")

MONGO_USERNAME = os.environ["MONGO_USER"]
MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]
MONGO_HOST = os.environ["MONGO_HOST"]
MONGO_PORT = os.environ["MONGO_PORT"]
MONGO_URL = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@mongo:{MONGO_PORT}/"

MONGO_DATABASE = os.environ["MONGO_DATABASE"]

# instanciate the mongo client
client = AsyncIOMotorClient(MONGO_URL)
engine = AIOEngine(client=client, database="example_db")
