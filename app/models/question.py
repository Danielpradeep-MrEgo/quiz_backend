from datetime import datetime
from bson import ObjectId

class QuestionModel:
    """Question data model"""
    
    @staticmethod
    def create_question(data):
        """Create a new question document"""
        question = {
            "quiz_id": ObjectId(data.get("quiz_id")),
            "type": data.get("type"),  # MCQ_SINGLE, MCQ_MULTI, TRUE_FALSE, TEXT
            "text": data.get("text"),
            "choices": data.get("choices", []),  # For MCQ and TRUE_FALSE
            "correct_text": data.get("correct_text", ""),  # For TEXT questions
            "points": data.get("points", 1),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        return question
    
    @staticmethod
    def update_question(existing_question, data):
        """Update an existing question document"""
        if "type" in data:
            existing_question["type"] = data["type"]
        if "text" in data:
            existing_question["text"] = data["text"]
        if "choices" in data:
            existing_question["choices"] = data["choices"]
        if "correct_text" in data:
            existing_question["correct_text"] = data["correct_text"]
        if "points" in data:
            existing_question["points"] = data["points"]
        existing_question["updated_at"] = datetime.utcnow()
        return existing_question
    
    @staticmethod
    def to_dict(question, include_correct_answers=False):
        """Convert question document to dictionary with string IDs"""
        if not question:
            return None
        
        choices = []
        for choice in question.get("choices", []):
            choice_dict = {
                "id": str(choice.get("_id", "")),
                "text": choice.get("text", "")
            }
            if include_correct_answers:
                choice_dict["is_correct"] = choice.get("is_correct", False)
            choices.append(choice_dict)
        
        question_dict = {
            "id": str(question["_id"]),
            "quiz_id": str(question.get("quiz_id", "")),
            "type": question.get("type"),
            "text": question.get("text"),
            "choices": choices,
            "points": question.get("points", 1),
            "created_at": question.get("created_at").isoformat() if question.get("created_at") else None,
            "updated_at": question.get("updated_at").isoformat() if question.get("updated_at") else None
        }
        
        if include_correct_answers and question.get("type") == "TEXT":
            question_dict["correct_text"] = question.get("correct_text", "")
        
        return question_dict

