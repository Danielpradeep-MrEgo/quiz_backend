from flask import jsonify
from bson import ObjectId
from bson.errors import InvalidId
from app.models.quiz import QuizModel
from app.models.question import QuestionModel
from app.utils.slug import generate_unique_slug

class AdminController:
    """Controller for admin operations"""
    
    def __init__(self, db):
        self.db = db
        self.quizzes_collection = db.quizzes
        self.questions_collection = db.questions
    
    def create_quiz(self, data):
        """Create a new quiz"""
        if not data.get("title"):
            return {"error": "Title is required"}, 400
        
        # Generate unique slug
        slug = generate_unique_slug(self.db, data.get("title"))
        data["slug"] = slug
        
        quiz = QuizModel.create_quiz(data)
        result = self.quizzes_collection.insert_one(quiz)
        quiz["_id"] = result.inserted_id
        
        return jsonify(QuizModel.to_dict(quiz)), 201
    
    def get_all_quizzes(self):
        """Get all quizzes with question counts"""
        quizzes = list(self.quizzes_collection.find().sort("created_at", -1))
        
        # Get question counts for each quiz
        quiz_list = []
        for quiz in quizzes:
            quiz_dict = QuizModel.to_dict(quiz)
            # Count questions for this quiz
            question_count = self.questions_collection.count_documents({"quiz_id": quiz["_id"]})
            quiz_dict["question_count"] = question_count
            quiz_list.append(quiz_dict)
        
        return jsonify(quiz_list), 200
    
    def get_quiz_by_id(self, quiz_id, include_questions=False):
        """Get a quiz by ID"""
        try:
            quiz = self.quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
            if not quiz:
                return {"error": "Quiz not found"}, 404
            
            quiz_dict = QuizModel.to_dict(quiz)
            
            # Get question count
            question_count = self.questions_collection.count_documents({"quiz_id": ObjectId(quiz_id)})
            quiz_dict["question_count"] = question_count
            
            # If include_questions is True, fetch and include all questions
            if include_questions:
                questions = list(
                    self.questions_collection.find({"quiz_id": ObjectId(quiz_id)})
                    .sort("created_at", 1)
                )
                quiz_dict["questions"] = [
                    QuestionModel.to_dict(q, include_correct_answers=True)
                    for q in questions
                ]
            
            return jsonify(quiz_dict), 200
        except InvalidId:
            return {"error": "Invalid quiz ID"}, 400
    
    def update_quiz(self, quiz_id, data):
        """Update a quiz"""
        try:
            quiz = self.quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
            if not quiz:
                return {"error": "Quiz not found"}, 404
            
            # If title is being updated, regenerate slug
            if "title" in data and data["title"] != quiz.get("title"):
                data["slug"] = generate_unique_slug(self.db, data["title"], exclude_id=quiz_id)
            
            updated_quiz = QuizModel.update_quiz(quiz, data)
            self.quizzes_collection.update_one(
                {"_id": ObjectId(quiz_id)},
                {"$set": updated_quiz}
            )
            
            return jsonify(QuizModel.to_dict(updated_quiz)), 200
        except InvalidId:
            return {"error": "Invalid quiz ID"}, 400
    
    def delete_quiz(self, quiz_id):
        """Delete a quiz and all its questions"""
        try:
            # Check if quiz exists
            quiz = self.quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
            if not quiz:
                return {"error": "Quiz not found"}, 404
            
            # Delete all questions for this quiz
            self.questions_collection.delete_many({"quiz_id": ObjectId(quiz_id)})
            
            # Delete the quiz
            self.quizzes_collection.delete_one({"_id": ObjectId(quiz_id)})
            
            return {"message": "Quiz deleted successfully"}, 200
        except InvalidId:
            return {"error": "Invalid quiz ID"}, 400
    
    def create_question(self, quiz_id, data):
        """Create a new question for a quiz"""
        try:
            # Verify quiz exists
            quiz = self.quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
            if not quiz:
                return {"error": "Quiz not found"}, 404
            
            # Validate question data
            if not data.get("text"):
                return {"error": "Question text is required"}, 400
            
            question_type = data.get("type")
            if question_type not in ["MCQ_SINGLE", "MCQ_MULTI", "TRUE_FALSE", "TEXT"]:
                return {"error": "Invalid question type"}, 400
            
            # Validate choices for MCQ and TRUE_FALSE
            if question_type in ["MCQ_SINGLE", "MCQ_MULTI", "TRUE_FALSE"]:
                choices = data.get("choices", [])
                if not choices or len(choices) < 2:
                    return {"error": "At least 2 choices are required for MCQ/TRUE_FALSE questions"}, 400
                
                # Generate IDs for choices if not provided
                for choice in choices:
                    if "_id" not in choice:
                        choice["_id"] = ObjectId()
            
            # Validate correct_text for TEXT questions
            if question_type == "TEXT":
                if not data.get("correct_text"):
                    return {"error": "correct_text is required for TEXT questions"}, 400
            
            data["quiz_id"] = quiz_id
            question = QuestionModel.create_question(data)
            result = self.questions_collection.insert_one(question)
            question["_id"] = result.inserted_id
            
            return jsonify(QuestionModel.to_dict(question, include_correct_answers=True)), 201
        except InvalidId:
            return {"error": "Invalid quiz ID"}, 400
    
    def update_question(self, question_id, data):
        """Update a question"""
        try:
            question = self.questions_collection.find_one({"_id": ObjectId(question_id)})
            if not question:
                return {"error": "Question not found"}, 404
            
            # Validate question type if being updated
            if "type" in data:
                if data["type"] not in ["MCQ_SINGLE", "MCQ_MULTI", "TRUE_FALSE", "TEXT"]:
                    return {"error": "Invalid question type"}, 400
            
            # Validate choices if being updated
            if "choices" in data:
                question_type = data.get("type", question.get("type"))
                if question_type in ["MCQ_SINGLE", "MCQ_MULTI", "TRUE_FALSE"]:
                    choices = data["choices"]
                    if not choices or len(choices) < 2:
                        return {"error": "At least 2 choices are required"}, 400
                    
                    # Generate IDs for new choices if not provided
                    for choice in choices:
                        if "_id" not in choice:
                            choice["_id"] = ObjectId()
            
            updated_question = QuestionModel.update_question(question, data)
            self.questions_collection.update_one(
                {"_id": ObjectId(question_id)},
                {"$set": updated_question}
            )
            
            return jsonify(QuestionModel.to_dict(updated_question, include_correct_answers=True)), 200
        except InvalidId:
            return {"error": "Invalid question ID"}, 400
    
    def delete_question(self, question_id):
        """Delete a question"""
        try:
            question = self.questions_collection.find_one({"_id": ObjectId(question_id)})
            if not question:
                return {"error": "Question not found"}, 404
            
            self.questions_collection.delete_one({"_id": ObjectId(question_id)})
            return {"message": "Question deleted successfully"}, 200
        except InvalidId:
            return {"error": "Invalid question ID"}, 400
    
    def get_question_by_id(self, question_id):
        """Get a question by ID with correct answers"""
        try:
            question = self.questions_collection.find_one({"_id": ObjectId(question_id)})
            if not question:
                return {"error": "Question not found"}, 404
            return jsonify(QuestionModel.to_dict(question, include_correct_answers=True)), 200
        except InvalidId:
            return {"error": "Invalid question ID"}, 400
    
    def get_quiz_questions(self, quiz_id):
        """Get all questions for a quiz with correct answers"""
        try:
            # Verify quiz exists
            quiz = self.quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
            if not quiz:
                return {"error": "Quiz not found"}, 404
            
            questions = list(
                self.questions_collection.find({"quiz_id": ObjectId(quiz_id)})
                .sort("created_at", 1)
            )
            
            return jsonify([
                QuestionModel.to_dict(q, include_correct_answers=True)
                for q in questions
            ]), 200
        except InvalidId:
            return {"error": "Invalid quiz ID"}, 400

