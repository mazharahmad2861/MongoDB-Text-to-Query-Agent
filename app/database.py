from pymongo import MongoClient

from app.config import MONGODB_URI, DATABASE_NAME
from langchain_mongodb.agent_toolkit.database import MongoDBDatabase


# Standard MongoDB client
mongodb_client = MongoClient(MONGODB_URI)


# Test connection
mongodb_client.admin.command("ping")


# LangChain MongoDB database wrapper
db = MongoDBDatabase.from_connection_string(
    connection_string=MONGODB_URI,
    database=DATABASE_NAME,
)