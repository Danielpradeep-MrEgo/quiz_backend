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

# MongoDB Setup - Read from environment variables
# Railway sets these as environment variables, .env file is for local dev only
mongo_uri = os.environ.get("MONGO_URI") or Config.MONGO_URI
db_name = os.environ.get("DB_NAME") or Config.DB_NAME or "quiz_management"

# Debug logging (check Railway logs to see these)
print("=" * 50)
print("ENVIRONMENT VARIABLE DEBUG:")
print(f"MONGO_URI in os.environ: {'MONGO_URI' in os.environ}")
print(f"MONGO_URI value (first 50 chars): {str(os.environ.get('MONGO_URI', 'NOT_SET'))[:50]}")
print(f"Config.MONGO_URI (first 50 chars): {str(Config.MONGO_URI)[:50]}")
print(f"Final mongo_uri used: {str(mongo_uri)[:50] if mongo_uri else 'None'}")
print("=" * 50)

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
    print(os.environ.get("MONGO_URI"))
    response = {
        "status": status,
        "mongodb_connected": db is not None
    }
    if error_message:
        response["error"] = error_message
    return jsonify(response), 200 if db is not None else 503

if __name__ == "__main__":
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
