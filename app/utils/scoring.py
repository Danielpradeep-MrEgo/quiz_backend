from bson import ObjectId
from bson.errors import InvalidId

def grade_answer(question, answer_data):
    """
    Grade a single answer based on question type
    
    Args:
        question: Question document from database
        answer_data: Dict with 'selected_choice_ids' (list) and/or 'text_answer' (str)
    
    Returns:
        tuple: (points_awarded, is_correct)
    """
    question_type = question.get("type")
    points = question.get("points", 1)
    
    if question_type == "MCQ_SINGLE":
        return grade_mcq_single(question, answer_data, points)
    elif question_type == "MCQ_MULTI":
        return grade_mcq_multi(question, answer_data, points)
    elif question_type == "TRUE_FALSE":
        return grade_true_false(question, answer_data, points)
    elif question_type == "TEXT":
        return grade_text(question, answer_data, points)
    else:
        return (0, False)

def grade_mcq_single(question, answer_data, points):
    """Grade a single-choice MCQ question"""
    try:
        selected_ids = [ObjectId(cid) for cid in answer_data.get("selected_choice_ids", [])]
    except (InvalidId, TypeError):
        return (0, False)
    
    if len(selected_ids) != 1:
        return (0, False)
    
    selected_id = selected_ids[0]
    choices = question.get("choices", [])
    
    # Find the selected choice
    selected_choice = None
    for choice in choices:
        if choice.get("_id") == selected_id:
            selected_choice = choice
            break
    
    if not selected_choice:
        return (0, False)
    
    is_correct = selected_choice.get("is_correct", False)
    return (points if is_correct else 0, is_correct)

def grade_mcq_multi(question, answer_data, points):
    """Grade a multi-choice MCQ question"""
    try:
        selected_ids = set(ObjectId(cid) for cid in answer_data.get("selected_choice_ids", []))
    except (InvalidId, TypeError):
        return (0, False)
    
    choices = question.get("choices", [])
    
    # Get all correct choice IDs
    correct_ids = set()
    for choice in choices:
        if choice.get("is_correct", False):
            choice_id = choice.get("_id")
            if choice_id:
                correct_ids.add(choice_id)
    
    # Check if selected set matches correct set exactly
    is_correct = selected_ids == correct_ids
    return (points if is_correct else 0, is_correct)

def grade_true_false(question, answer_data, points):
    """Grade a true/false question"""
    try:
        selected_ids = [ObjectId(cid) for cid in answer_data.get("selected_choice_ids", [])]
    except (InvalidId, TypeError):
        return (0, False)
    
    if len(selected_ids) != 1:
        return (0, False)
    
    selected_id = selected_ids[0]
    choices = question.get("choices", [])
    
    # Find the selected choice
    selected_choice = None
    for choice in choices:
        if choice.get("_id") == selected_id:
            selected_choice = choice
            break
    
    if not selected_choice:
        return (0, False)
    
    is_correct = selected_choice.get("is_correct", False)
    return (points if is_correct else 0, is_correct)

def grade_text(question, answer_data, points):
    """Grade a text answer question (exact match, case-insensitive)"""
    user_answer = answer_data.get("text_answer", "").strip()
    correct_answer = question.get("correct_text", "").strip()
    
    is_correct = user_answer.lower() == correct_answer.lower()
    return (points if is_correct else 0, is_correct)

def get_correct_answers(question):
    """
    Extract correct answers from a question for response
    
    Returns:
        dict: Correct answer information
    """
    question_type = question.get("type")
    result = {
        "question_id": str(question.get("_id")),
        "type": question_type
    }
    
    if question_type in ["MCQ_SINGLE", "MCQ_MULTI", "TRUE_FALSE"]:
        correct_choice_ids = []
        correct_choice_texts = []
        for choice in question.get("choices", []):
            if choice.get("is_correct", False):
                correct_choice_ids.append(str(choice.get("_id", "")))
                correct_choice_texts.append(choice.get("text", ""))
        
        result["correct_choice_ids"] = correct_choice_ids
        result["correct_choice_texts"] = correct_choice_texts
    elif question_type == "TEXT":
        result["correct_text"] = question.get("correct_text", "")
    
    return result

