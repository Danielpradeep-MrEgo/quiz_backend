from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId

class AttemptModel:
    """Attempt data model"""
    
    @staticmethod
    def create_attempt(data):
        """Create a new attempt document"""
        try:
            quiz_id = ObjectId(data.get("quiz_id"))
        except (InvalidId, TypeError):
            raise ValueError(f"Invalid quiz_id: {data.get('quiz_id')}")
        
        attempt = {
            "quiz_id": quiz_id,
            "name": data.get("name"),
            "email": data.get("email"),
            "submitted_at": datetime.utcnow(),
            "score": data.get("score", 0),
            "max_score": data.get("max_score", 0),
            "answers": data.get("answers", [])
        }
        return attempt
    
    @staticmethod
    def to_dict(attempt):
        """Convert attempt document to dictionary with string IDs"""
        if not attempt:
            return None
        
        answers = []
        for answer in attempt.get("answers", []):
            answer_dict = {
                "question_id": str(answer.get("question_id", "")),
                "selected_choice_ids": [str(cid) for cid in answer.get("selected_choice_ids", [])],
                "text_answer": answer.get("text_answer", ""),
                "points_awarded": answer.get("points_awarded", 0)
            }
            answers.append(answer_dict)
        
        attempt_dict = {
            "id": str(attempt["_id"]),
            "quiz_id": str(attempt.get("quiz_id", "")),
            "name": attempt.get("name"),
            "email": attempt.get("email"),
            "submitted_at": attempt.get("submitted_at").isoformat() if attempt.get("submitted_at") else None,
            "score": attempt.get("score", 0),
            "max_score": attempt.get("max_score", 0),
            "answers": answers
        }
        return attempt_dict

