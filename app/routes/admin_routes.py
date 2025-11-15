from flask import Blueprint, request
from app.controllers.admin_controller import AdminController

def create_admin_blueprint(db):
    """Create and configure admin blueprint"""
    admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
    controller = AdminController(db)
    
    @admin_bp.route("/quizzes", methods=["POST"])
    def create_quiz():
        """Create a new quiz"""
        data = request.get_json()
        return controller.create_quiz(data)
    
    @admin_bp.route("/quizzes", methods=["GET"])
    def get_all_quizzes():
        """Get all quizzes"""
        return controller.get_all_quizzes()
    
    @admin_bp.route("/quizzes/<quiz_id>", methods=["GET"])
    def get_quiz(quiz_id):
        """Get a quiz by ID (optionally with questions)"""
        include_questions = request.args.get("include_questions", "false").lower() == "true"
        return controller.get_quiz_by_id(quiz_id, include_questions=include_questions)
    
    @admin_bp.route("/quizzes/<quiz_id>", methods=["PUT"])
    def update_quiz(quiz_id):
        """Update a quiz"""
        data = request.get_json()
        return controller.update_quiz(quiz_id, data)
    
    @admin_bp.route("/quizzes/<quiz_id>", methods=["DELETE"])
    def delete_quiz(quiz_id):
        """Delete a quiz"""
        return controller.delete_quiz(quiz_id)
    
    @admin_bp.route("/quizzes/<quiz_id>/questions", methods=["POST"])
    def create_question(quiz_id):
        """Create a new question for a quiz"""
        data = request.get_json()
        return controller.create_question(quiz_id, data)
    
    @admin_bp.route("/questions/<question_id>", methods=["PUT"])
    def update_question(question_id):
        """Update a question"""
        data = request.get_json()
        return controller.update_question(question_id, data)
    
    @admin_bp.route("/questions/<question_id>", methods=["DELETE"])
    def delete_question(question_id):
        """Delete a question"""
        return controller.delete_question(question_id)
    
    @admin_bp.route("/questions/<question_id>", methods=["GET"])
    def get_question(question_id):
        """Get a question by ID with correct answers"""
        return controller.get_question_by_id(question_id)
    
    @admin_bp.route("/quizzes/<quiz_id>/questions", methods=["GET"])
    def get_quiz_questions(quiz_id):
        """Get all questions for a quiz with correct answers"""
        return controller.get_quiz_questions(quiz_id)
    
    return admin_bp

