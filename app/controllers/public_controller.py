from flask import jsonify
from bson import ObjectId
from bson.errors import InvalidId
from app.models.quiz import QuizModel
from app.models.question import QuestionModel
from app.models.attempt import AttemptModel
from app.utils.scoring import grade_answer, get_correct_answers

class PublicController:
    """Controller for public operations"""
    
    def __init__(self, db):
        self.db = db
        self.quizzes_collection = db.quizzes
        self.questions_collection = db.questions
        self.attempts_collection = db.attempts
    
    def get_published_quizzes(self):
        """Get all published quizzes"""
        quizzes = list(
            self.quizzes_collection.find({"published": True})
            .sort("created_at", -1)
        )
        return jsonify([QuizModel.to_dict(q) for q in quizzes]), 200
    
    def get_quiz_by_slug(self, slug_or_id):
        """Get a published quiz by slug or ID (without correct answers)"""
        # Try to find by ID first (if it's a valid ObjectId)
        quiz = None
        try:
            quiz = self.quizzes_collection.find_one({"_id": ObjectId(slug_or_id), "published": True})
        except (InvalidId, ValueError):
            pass
        
        # If not found by ID, try by slug
        if not quiz:
            quiz = self.quizzes_collection.find_one({"slug": slug_or_id, "published": True})
        
        if not quiz:
            return {"error": "Quiz not found"}, 404
        
        # Get questions without correct answers
        questions = list(
            self.questions_collection.find({"quiz_id": quiz["_id"]})
            .sort("created_at", 1)
        )
        
        quiz_dict = QuizModel.to_dict(quiz)
        quiz_dict["questions"] = [
            QuestionModel.to_dict(q, include_correct_answers=False)
            for q in questions
        ]
        
        return jsonify(quiz_dict), 200
    
    def submit_attempt(self, slug_or_id, data):
        """Submit a quiz attempt and auto-grade it"""
        # Try to find by ID first (if it's a valid ObjectId)
        quiz = None
        try:
            quiz = self.quizzes_collection.find_one({"_id": ObjectId(slug_or_id), "published": True})
        except (InvalidId, ValueError):
            pass
        
        # If not found by ID, try by slug
        if not quiz:
            quiz = self.quizzes_collection.find_one({"slug": slug_or_id, "published": True})
        
        if not quiz:
            return {"error": "Quiz not found"}, 404
        
        # Get all questions for this quiz
        questions = list(
            self.questions_collection.find({"quiz_id": quiz["_id"]})
            .sort("created_at", 1)
        )
        
        if not questions:
            return {"error": "Quiz has no questions"}, 400
        
        # Validate submission data
        # if not data.get("name"):
        #     return {"error": "Name is required"}, 400
        # if not data.get("email"):
        #     return {"error": "Email is required"}, 400
        
        answers_data = data.get("answers", [])
        if len(answers_data) != len(questions):
            return {"error": f"Expected {len(questions)} answers, got {len(answers_data)}"}, 400
        
        # Grade each answer
        total_score = 0
        max_score = sum(q.get("points", 1) for q in questions)
        graded_answers = []
        correct_answers_summary = []
        
        # Create a map of question_id to question for quick lookup
        question_map = {str(q["_id"]): q for q in questions}
        
        for answer_data in answers_data:
            question_id = answer_data.get("question_id")
            if not question_id:
                return {"error": "question_id is required for each answer"}, 400
            
            question = question_map.get(question_id)
            if not question:
                return {"error": f"Question {question_id} not found"}, 400
            
            # Grade the answer
            points_awarded, is_correct = grade_answer(question, answer_data)
            total_score += points_awarded
            
            # Store graded answer
            try:
                graded_answer = {
                    "question_id": ObjectId(question_id),
                    "selected_choice_ids": [ObjectId(cid) for cid in answer_data.get("selected_choice_ids", [])],
                    "text_answer": answer_data.get("text_answer", ""),
                    "points_awarded": points_awarded
                }
                graded_answers.append(graded_answer)
            except (InvalidId, TypeError) as e:
                return {"error": f"Invalid ID format in answer: {str(e)}"}, 400
            
            # Get correct answer for response
            correct_answer_info = get_correct_answers(question)
            correct_answer_info["is_correct"] = is_correct
            correct_answer_info["points_awarded"] = points_awarded
            correct_answer_info["max_points"] = question.get("points", 1)
            correct_answers_summary.append(correct_answer_info)
        
        # Create attempt document
        attempt_data = {
            "quiz_id": str(quiz["_id"]),
            "name": data.get("name"),
            "email": data.get("email"),
            "score": total_score,
            "max_score": max_score,
            "answers": graded_answers
        }
        
        try:
            attempt = AttemptModel.create_attempt(attempt_data)
            result = self.attempts_collection.insert_one(attempt)
            attempt["_id"] = result.inserted_id
        except ValueError as e:
            return {"error": str(e)}, 400
        
        # Prepare response
        response = {
            "attempt_id": str(attempt["_id"]),
            "quiz_id": str(quiz["_id"]),
            "quiz_title": quiz.get("title"),
            "name": data.get("name"),
            "email": data.get("email"),
            "score": total_score,
            "max_score": max_score,
            "percentage": round((total_score / max_score * 100) if max_score > 0 else 0, 2),
            "submitted_at": attempt.get("submitted_at").isoformat(),
            "answers": correct_answers_summary
        }
        
        return jsonify(response), 201

