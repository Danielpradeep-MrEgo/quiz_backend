from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from config import Config
from app.routes.admin_routes import create_admin_blueprint
from app.routes.public_routes import create_public_blueprint
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# MongoDB Setup
mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME", "quiz_management")

if not mongo_uri:
    raise ValueError("MONGO_URI environment variable is required")

client = MongoClient(mongo_uri)
db = client[db_name]

# Register blueprints
admin_bp = create_admin_blueprint(db)
public_bp = create_public_blueprint(db)
app.register_blueprint(admin_bp)
app.register_blueprint(public_bp)

@app.route("/")
def home():
    return jsonify({"message": "Quiz Management System API is running!"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

# Export the Flask app for Vercel
handler = app

