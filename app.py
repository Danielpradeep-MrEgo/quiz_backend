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

# Initialize variables
client = None
db = None
error_message = None

if not mongo_uri:
    error_message = "MONGO_URI environment variable is not set"
    print(f"WARNING: {error_message}")
else:
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        print(f"Successfully connected to MongoDB: {db_name}")
    except Exception as e:
        error_message = f"MongoDB connection failed: {str(e)}"
        print(f"ERROR: {error_message}")
        client = None
        db = None

# Register blueprints only if db is available
if db is not None:
    try:
        admin_bp = create_admin_blueprint(db)
        public_bp = create_public_blueprint(db)
        app.register_blueprint(admin_bp)
        app.register_blueprint(public_bp)
        print("Blueprints registered successfully")
    except Exception as e:
        error_message = f"Failed to register blueprints: {str(e)}"
        print(f"ERROR: {error_message}")

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
