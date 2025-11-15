from datetime import datetime
from bson import ObjectId

class QuizModel:
    """Quiz data model"""
    
    @staticmethod
    def create_quiz(data):
        """Create a new quiz document"""
        quiz = {
            "title": data.get("title"),
            "slug": data.get("slug"),
            "description": data.get("description", ""),
            "published": data.get("published", False),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        return quiz
    
    @staticmethod
    def update_quiz(existing_quiz, data):
        """Update an existing quiz document"""
        if "title" in data:
            existing_quiz["title"] = data["title"]
        if "slug" in data:
            existing_quiz["slug"] = data["slug"]
        if "description" in data:
            existing_quiz["description"] = data["description"]
        if "published" in data:
            existing_quiz["published"] = data["published"]
        existing_quiz["updated_at"] = datetime.utcnow()
        return existing_quiz
    
    @staticmethod
    def to_dict(quiz):
        """Convert quiz document to dictionary with string ID"""
        if not quiz:
            return None
        quiz_dict = {
            "id": str(quiz["_id"]),
            "title": quiz.get("title"),
            "slug": quiz.get("slug"),
            "description": quiz.get("description"),
            "published": quiz.get("published", False),
            "created_at": quiz.get("created_at").isoformat() if quiz.get("created_at") else None,
            "updated_at": quiz.get("updated_at").isoformat() if quiz.get("updated_at") else None
        }
        return quiz_dict

