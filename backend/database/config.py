from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "DisasterPredict")

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    print(f"Connected to MongoDB successfully! Using database: {DB_NAME}")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
