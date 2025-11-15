import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME = os.environ.get("DB_NAME", "quiz_management")
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Flask settings
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
    PORT = int(os.environ.get("FLASK_PORT", "5000"))

