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
# Railway injects these at runtime
mongo_uri = os.getenv("MONGO_URI")  # Use getenv instead of environ.get
db_name = os.getenv("DB_NAME", "quiz_management")

# Extensive debugging - check Railway logs for this output
print("\n" + "="*60)
print("ENVIRONMENT VARIABLE DIAGNOSTICS:")
print("="*60)
print(f"All environment variables containing 'MONGO':")
for key, value in os.environ.items():
    if 'MONGO' in key.upper():
        # Show first 30 chars of value for security
        val_preview = value[:30] + "..." if len(value) > 30 else value
        print(f"  {key} = {val_preview} (length: {len(value)})")

print(f"\nMONGO_URI check:")
print(f"  'MONGO_URI' in os.environ: {'MONGO_URI' in os.environ}")
print(f"  os.getenv('MONGO_URI'): {os.getenv('MONGO_URI', 'NOT_FOUND')[:50] if os.getenv('MONGO_URI') else 'NOT_FOUND'}")
print(f"  os.environ.get('MONGO_URI'): {os.environ.get('MONGO_URI', 'NOT_FOUND')[:50] if os.environ.get('MONGO_URI') else 'NOT_FOUND'}")

# Try alternative names Railway might use
alt_names = ['MONGO_URI', 'MONGODB_URI', 'DATABASE_URL', 'MONGO_URL']
for alt_name in alt_names:
    if alt_name in os.environ:
        print(f"  Found alternative: {alt_name}")

print(f"\nFinal values:")
print(f"  mongo_uri: {mongo_uri[:50] + '...' if mongo_uri and len(mongo_uri) > 50 else mongo_uri or 'None'}")
print(f"  db_name: {db_name}")
print("="*60 + "\n")

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
