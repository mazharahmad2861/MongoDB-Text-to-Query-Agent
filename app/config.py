import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not set in .env")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in .env")

DATABASE_NAME = "sample_mflix"
MODEL_NAME = "gpt-4o-mini"