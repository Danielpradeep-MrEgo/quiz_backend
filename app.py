from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from config import Config
from app.routes.admin_routes import create_admin_blueprint
from app.routes.public_routes import create_public_blueprint
import os

# Load environment variables from .env file (for local development)
# On Railway, this will use the environment variables set in the dashboard
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# MongoDB Setup - Read directly from environment variables
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME", "quiz_management")

# Initialize variables
client = None
db = None
error_message = None

if not mongo_uri:
    error_message = "MONGO_URI environment variable is not set"
else:
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
    except Exception as e:
        error_message = f"MongoDB connection failed: {str(e)}"
        client = None
        db = None

# Register blueprints only if db is available
if db is not None:
    try:
        admin_bp = create_admin_blueprint(db)
        public_bp = create_public_blueprint(db)
        app.register_blueprint(admin_bp)
        app.register_blueprint(public_bp)
    except Exception as e:
        error_message = f"Failed to register blueprints: {str(e)}"

@app.route("/")
def home():
    if db is None:
        return jsonify({
            "error": "MongoDB connection not configured",
            "message": error_message or "Please set MONGO_URI environment variable"
        }), 500
    return jsonify({"message": "Quiz Management System API is running!"})

@app.route("/health")
def health():
    status = "healthy" if db is not None else "unhealthy"
    response = {
        "status": status,
        "mongodb_connected": db is not None
    }
    if error_message:
        response["error"] = error_message
    return jsonify(response), 200 if db is not None else 503

if __name__ == "__main__":
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
