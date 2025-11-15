import os

from pymongo import MongoClient
from config import Config

# Global database connection
db = None
client = None

print(os.environ.get("MONGO_URI"))
def init_db():
    """Initialize MongoDB connection"""
    global db, client
    
    try:
        client = MongoClient(os.environ.get("MONGO_URI"))
        db = client[os.environ.get("DB_NAME")]
        return db
    except Exception as e:
        print(f"✗ Error connecting to MongoDB: {e}")
        raise

def get_db():
    """Get database instance"""
    global db
    if db is None:
        init_db()
    return db

