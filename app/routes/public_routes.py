from flask import Blueprint, request
from app.controllers.public_controller import PublicController

def create_public_blueprint(db):
    """Create and configure public blueprint"""
    public_bp = Blueprint("public", __name__, url_prefix="/quizzes")
    controller = PublicController(db)
    
    @public_bp.route("", methods=["GET"])
    def get_published_quizzes():
        """Get all published quizzes"""
        return controller.get_published_quizzes()
    
    @public_bp.route("/<slug_or_id>", methods=["GET"])
    def get_quiz_by_slug(slug_or_id):
        """Get a published quiz by slug or ID"""
        return controller.get_quiz_by_slug(slug_or_id)
    
    @public_bp.route("/<slug_or_id>/attempt", methods=["POST"])
    def submit_attempt(slug_or_id):
        """Submit a quiz attempt"""
        data = request.get_json()
        return controller.submit_attempt(slug_or_id, data)
    
    return public_bp

