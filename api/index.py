import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from app.routes.admin_routes import create_admin_blueprint
from app.routes.public_routes import create_public_blueprint

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# MongoDB Setup
mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME", "quiz_management")

if not mongo_uri:
    # For Vercel, we'll allow it to fail gracefully and show error
    print("WARNING: MONGO_URI not set")
    client = None
    db = None
else:
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        print(f"Connected to MongoDB: {db_name}")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        client = None
        db = None

# Only register blueprints if db is available
if db:
    admin_bp = create_admin_blueprint(db)
    public_bp = create_public_blueprint(db)
    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)

@app.route("/")
def home():
    if not db:
        return jsonify({"error": "MongoDB connection not configured. Please set MONGO_URI environment variable."}), 500
    return jsonify({"message": "Quiz Management System API is running!"})

@app.route("/health")
def health():
    status = "healthy" if db else "unhealthy"
    return jsonify({
        "status": status,
        "mongodb_connected": db is not None
    })

# Export the Flask app for Vercel
# Vercel's @vercel/python builder automatically detects and wraps Flask apps
# The app variable is automatically exported

