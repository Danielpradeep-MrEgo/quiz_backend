# Quiz Management System Backend

A complete Flask + MongoDB backend for managing quizzes with admin and public APIs.

## 🚀 Features

- **Admin API**: Create, edit, delete quizzes and questions (no authentication required)
- **Public API**: List published quizzes, take quizzes, and auto-grade submissions
- **Question Types**: MCQ_SINGLE, MCQ_MULTI, TRUE_FALSE, TEXT
- **Auto-grading**: Automatic scoring with detailed feedback
- **Slug Generation**: Automatic URL-friendly slug generation for quizzes

## 📁 Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── admin_controller.py
│   │   └── public_controller.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── quiz.py
│   │   ├── question.py
│   │   └── attempt.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin_routes.py
│   │   └── public_routes.py
│   └── utils/
│       ├── __init__.py
│       ├── slug.py
│       └── scoring.py
├── app.py
├── config.py
├── requirements.txt
├── .env.example
└── README.md
```

## 🛠 Setup Instructions

### Local Development

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update with your MongoDB connection string:

```bash
cp .env.example .env
```

Edit `.env`:
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=quiz_management
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

#### 3. Run the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### 🚀 Deploy to Railway

**Quick Deploy:** See [DEPLOY_RAILWAY.md](DEPLOY_RAILWAY.md) for a 5-minute deployment guide.

**Detailed Guide:** See [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md) for comprehensive deployment instructions.

**Quick Steps:**
1. Push code to GitHub
2. Deploy from GitHub repo in Railway
3. Set environment variables (`MONGO_URI`, `DB_NAME`)
4. Deploy!

Your API will be live at `https://your-project.up.railway.app`

**Why Railway?**
- ✅ Simpler setup (no serverless wrappers needed)
- ✅ Better for MongoDB connections
- ✅ Uses your existing `app.py` directly
- ✅ Automatic port management

## 📡 API Endpoints

> **📖 For detailed API usage with examples, see [API_USAGE.md](API_USAGE.md)**

### Admin Endpoints (No Authentication)

#### Quizzes

- **POST** `/admin/quizzes` - Create a new quiz
- **GET** `/admin/quizzes` - Get all quizzes
- **GET** `/admin/quizzes/<quiz_id>` - Get a quiz by ID
- **PUT** `/admin/quizzes/<quiz_id>` - Update a quiz
- **DELETE** `/admin/quizzes/<quiz_id>` - Delete a quiz

#### Questions

- **POST** `/admin/quizzes/<quiz_id>/questions` - Create a question for a quiz
- **PUT** `/admin/questions/<question_id>` - Update a question
- **DELETE** `/admin/questions/<question_id>` - Delete a question

### Public Endpoints

- **GET** `/quizzes` - Get all published quizzes
- **GET** `/quizzes/<slug>` - Get a published quiz by slug (without correct answers)
- **POST** `/quizzes/<slug>/attempt` - Submit a quiz attempt (returns graded results)

## 📝 Example Requests

### 1. Create a Quiz

```bash
POST http://localhost:5000/admin/quizzes
Content-Type: application/json

{
  "title": "Python Basics Quiz",
  "description": "Test your Python knowledge",
  "published": true
}
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Python Basics Quiz",
  "slug": "python-basics-quiz",
  "description": "Test your Python knowledge",
  "published": true,
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

### 2. Create a MCQ_SINGLE Question

```bash
POST http://localhost:5000/admin/quizzes/<quiz_id>/questions
Content-Type: application/json

{
  "type": "MCQ_SINGLE",
  "text": "What is the output of print(2 + 2)?",
  "points": 5,
  "choices": [
    {"text": "3", "is_correct": false},
    {"text": "4", "is_correct": true},
    {"text": "5", "is_correct": false}
  ]
}
```

### 3. Create a MCQ_MULTI Question

```bash
POST http://localhost:5000/admin/quizzes/<quiz_id>/questions
Content-Type: application/json

{
  "type": "MCQ_MULTI",
  "text": "Which of the following are Python data types?",
  "points": 10,
  "choices": [
    {"text": "int", "is_correct": true},
    {"text": "string", "is_correct": true},
    {"text": "char", "is_correct": false},
    {"text": "list", "is_correct": true}
  ]
}
```

### 4. Create a TRUE_FALSE Question

```bash
POST http://localhost:5000/admin/quizzes/<quiz_id>/questions
Content-Type: application/json

{
  "type": "TRUE_FALSE",
  "text": "Python is a compiled language.",
  "points": 3,
  "choices": [
    {"text": "True", "is_correct": false},
    {"text": "False", "is_correct": true}
  ]
}
```

### 5. Create a TEXT Question

```bash
POST http://localhost:5000/admin/quizzes/<quiz_id>/questions
Content-Type: application/json

{
  "type": "TEXT",
  "text": "What keyword is used to define a function in Python?",
  "points": 5,
  "correct_text": "def"
}
```

### 6. Get Published Quiz by Slug

```bash
GET http://localhost:5000/quizzes/python-basics-quiz
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Python Basics Quiz",
  "slug": "python-basics-quiz",
  "description": "Test your Python knowledge",
  "published": true,
  "questions": [
    {
      "id": "507f1f77bcf86cd799439012",
      "type": "MCQ_SINGLE",
      "text": "What is the output of print(2 + 2)?",
      "points": 5,
      "choices": [
        {"id": "...", "text": "3"},
        {"id": "...", "text": "4"},
        {"id": "...", "text": "5"}
      ]
    }
  ]
}
```

### 7. Submit Quiz Attempt

```bash
POST http://localhost:5000/quizzes/python-basics-quiz/attempt
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "answers": [
    {
      "question_id": "507f1f77bcf86cd799439012",
      "selected_choice_ids": ["507f1f77bcf86cd799439013"]
    },
    {
      "question_id": "507f1f77bcf86cd799439014",
      "selected_choice_ids": ["507f1f77bcf86cd799439015", "507f1f77bcf86cd799439016"]
    },
    {
      "question_id": "507f1f77bcf86cd799439017",
      "selected_choice_ids": ["507f1f77bcf86cd799439018"]
    },
    {
      "question_id": "507f1f77bcf86cd799439019",
      "text_answer": "def"
    }
  ]
}
```

**Response:**
```json
{
  "attempt_id": "507f1f77bcf86cd799439020",
  "quiz_id": "507f1f77bcf86cd799439011",
  "quiz_title": "Python Basics Quiz",
  "name": "John Doe",
  "email": "john@example.com",
  "score": 18,
  "max_score": 23,
  "percentage": 78.26,
  "submitted_at": "2024-01-01T12:30:00",
  "answers": [
    {
      "question_id": "507f1f77bcf86cd799439012",
      "type": "MCQ_SINGLE",
      "is_correct": true,
      "points_awarded": 5,
      "max_points": 5,
      "correct_choice_ids": ["507f1f77bcf86cd799439013"],
      "correct_choice_texts": ["4"]
    },
    {
      "question_id": "507f1f77bcf86cd799439014",
      "type": "MCQ_MULTI",
      "is_correct": true,
      "points_awarded": 10,
      "max_points": 10,
      "correct_choice_ids": ["507f1f77bcf86cd799439015", "507f1f77bcf86cd799439016"],
      "correct_choice_texts": ["int", "list"]
    },
    {
      "question_id": "507f1f77bcf86cd799439017",
      "type": "TRUE_FALSE",
      "is_correct": false,
      "points_awarded": 0,
      "max_points": 3,
      "correct_choice_ids": ["507f1f77bcf86cd799439018"],
      "correct_choice_texts": ["False"]
    },
    {
      "question_id": "507f1f77bcf86cd799439019",
      "type": "TEXT",
      "is_correct": true,
      "points_awarded": 5,
      "max_points": 5,
      "correct_text": "def"
    }
  ]
}
```

## 🎯 Question Types

### MCQ_SINGLE
- Single choice multiple choice question
- User must select exactly one choice
- Points awarded if the selected choice is correct

### MCQ_MULTI
- Multiple choice question with multiple correct answers
- User must select all correct choices (exact match)
- Points awarded only if all correct choices are selected and no incorrect ones

### TRUE_FALSE
- True/False question
- User must select either True or False
- Points awarded if the selected choice is correct

### TEXT
- Text input question
- User provides a text answer
- Points awarded if answer matches correct_text (case-insensitive)

## 🔧 Scoring Logic

- **MCQ_SINGLE**: Full points if correct choice selected, 0 otherwise
- **MCQ_MULTI**: Full points only if exact set of correct choices selected, 0 otherwise
- **TRUE_FALSE**: Full points if correct choice selected, 0 otherwise
- **TEXT**: Full points if answer matches correct_text (case-insensitive), 0 otherwise

## 📦 Dependencies

- Flask 3.1.2
- flask-cors 6.0.1
- pymongo 4.15.4
- python-dotenv 1.2.1

## 🚨 Important Notes

- **No Authentication**: This backend has no authentication. In production, add proper authentication.
- **MongoDB Atlas**: Make sure your MongoDB Atlas cluster allows connections from your IP address.
- **CORS**: CORS is enabled for all origins. Configure appropriately for production.

## 📚 Additional Documentation

- **[API_USAGE.md](API_USAGE.md)** - Complete API usage guide with cURL, Python, and JavaScript examples
- **[README.md](README.md)** - This file (setup and overview)

## 📄 License

This project is provided as-is for educational purposes.

