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
client = MongoClient(os.environ.get("MONGO_URI"))
db = client[os.environ.get("DB_NAME")]

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

if __name__ == "__main__":
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
