# Quiz Management System - API Usage Guide

Complete guide with examples for all API endpoints.

## 📋 Table of Contents

- [Base URL](#base-url)
- [Admin API - Quizzes](#admin-api---quizzes)
- [Admin API - Questions](#admin-api---questions)
- [Public API](#public-api)
- [Complete Workflow Example](#complete-workflow-example)

---

## Base URL

```
http://localhost:5000
```

All endpoints return JSON responses.

---

## Admin API - Quizzes

### 1. Create a Quiz

**Endpoint:** `POST /admin/quizzes`

**Request Body:**

```json
{
  "title": "Python Fundamentals Quiz",
  "description": "Test your knowledge of Python basics",
  "published": true
}
```

**cURL Example:**

```bash
curl -X POST http://localhost:5000/admin/quizzes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Fundamentals Quiz",
    "description": "Test your knowledge of Python basics",
    "published": true
  }'
```

**Python Example:**

```python
import requests

url = "http://localhost:5000/admin/quizzes"
data = {
    "title": "Python Fundamentals Quiz",
    "description": "Test your knowledge of Python basics",
    "published": True
}

response = requests.post(url, json=data)
print(response.json())
```

**Response (201 Created):**

```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Python Fundamentals Quiz",
  "slug": "python-fundamentals-quiz",
  "description": "Test your knowledge of Python basics",
  "published": true,
  "created_at": "2024-01-15T10:30:00.123456",
  "updated_at": "2024-01-15T10:30:00.123456"
}
```

---

### 2. Get All Quizzes

**Endpoint:** `GET /admin/quizzes`

**cURL Example:**

```bash
curl http://localhost:5000/admin/quizzes
```

**Python Example:**

```python
import requests

url = "http://localhost:5000/admin/quizzes"
response = requests.get(url)
quizzes = response.json()
print(quizzes)
```

**Response (200 OK):**

```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "title": "Python Fundamentals Quiz",
    "slug": "python-fundamentals-quiz",
    "description": "Test your knowledge of Python basics",
    "published": true,
    "created_at": "2024-01-15T10:30:00.123456",
    "updated_at": "2024-01-15T10:30:00.123456"
  },
  {
    "id": "507f1f77bcf86cd799439012",
    "title": "JavaScript Basics",
    "slug": "javascript-basics",
    "description": "Learn JavaScript fundamentals",
    "published": false,
    "created_at": "2024-01-14T09:20:00.123456",
    "updated_at": "2024-01-14T09:20:00.123456"
  }
]
```

---

### 3. Get Quiz by ID

**Endpoint:** `GET /admin/quizzes/<quiz_id>`

**cURL Example:**

```bash
curl http://localhost:5000/admin/quizzes/507f1f77bcf86cd799439011
```

**Python Example:**

```python
import requests

quiz_id = "507f1f77bcf86cd799439011"
url = f"http://localhost:5000/admin/quizzes/{quiz_id}"
response = requests.get(url)
quiz = response.json()
print(quiz)
```

**Response (200 OK):**

```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Python Fundamentals Quiz",
  "slug": "python-fundamentals-quiz",
  "description": "Test your knowledge of Python basics",
  "published": true,
  "created_at": "2024-01-15T10:30:00.123456",
  "updated_at": "2024-01-15T10:30:00.123456"
}
```

---

### 4. Update a Quiz

**Endpoint:** `PUT /admin/quizzes/<quiz_id>`

**Request Body:**

```json
{
  "title": "Advanced Python Quiz",
  "description": "Updated description",
  "published": false
}
```

**cURL Example:**

```bash
curl -X PUT http://localhost:5000/admin/quizzes/507f1f77bcf86cd799439011 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Advanced Python Quiz",
    "description": "Updated description",
    "published": false
  }'
```

**Python Example:**

```python
import requests

quiz_id = "507f1f77bcf86cd799439011"
url = f"http://localhost:5000/admin/quizzes/{quiz_id}"
data = {
    "title": "Advanced Python Quiz",
    "description": "Updated description",
    "published": False
}

response = requests.put(url, json=data)
print(response.json())
```

**Response (200 OK):**

```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Advanced Python Quiz",
  "slug": "advanced-python-quiz",
  "description": "Updated description",
  "published": false,
  "created_at": "2024-01-15T10:30:00.123456",
  "updated_at": "2024-01-15T11:45:00.123456"
}
```

---

### 5. Delete a Quiz

**Endpoint:** `DELETE /admin/quizzes/<quiz_id>`

**cURL Example:**

```bash
curl -X DELETE http://localhost:5000/admin/quizzes/507f1f77bcf86cd799439011
```

**Python Example:**

```python
import requests

quiz_id = "507f1f77bcf86cd799439011"
url = f"http://localhost:5000/admin/quizzes/{quiz_id}"
response = requests.delete(url)
print(response.json())
```

**Response (200 OK):**

```json
{
  "message": "Quiz deleted successfully"
}
```

---

## Admin API - Questions

### 1. Create a MCQ_SINGLE Question

**Endpoint:** `POST /admin/quizzes/<quiz_id>/questions`

**Request Body:**

```json
{
  "type": "MCQ_SINGLE",
  "text": "What is the output of print(2 + 2)?",
  "points": 5,
  "choices": [
    { "text": "3", "is_correct": false },
    { "text": "4", "is_correct": true },
    { "text": "5", "is_correct": false },
    { "text": "6", "is_correct": false }
  ]
}
```

**cURL Example:**

```bash
curl -X POST http://localhost:5000/admin/quizzes/507f1f77bcf86cd799439011/questions \
  -H "Content-Type: application/json" \
  -d '{
    "type": "MCQ_SINGLE",
    "text": "What is the output of print(2 + 2)?",
    "points": 5,
    "choices": [
      {"text": "3", "is_correct": false},
      {"text": "4", "is_correct": true},
      {"text": "5", "is_correct": false},
      {"text": "6", "is_correct": false}
    ]
  }'
```

**Python Example:**

```python
import requests

quiz_id = "507f1f77bcf86cd799439011"
url = f"http://localhost:5000/admin/quizzes/{quiz_id}/questions"

data = {
    "type": "MCQ_SINGLE",
    "text": "What is the output of print(2 + 2)?",
    "points": 5,
    "choices": [
        {"text": "3", "is_correct": False},
        {"text": "4", "is_correct": True},
        {"text": "5", "is_correct": False},
        {"text": "6", "is_correct": False}
    ]
}

response = requests.post(url, json=data)
print(response.json())
```

**Response (201 Created):**

```json
{
  "id": "507f1f77bcf86cd799439020",
  "quiz_id": "507f1f77bcf86cd799439011",
  "type": "MCQ_SINGLE",
  "text": "What is the output of print(2 + 2)?",
  "points": 5,
  "choices": [
    { "id": "507f1f77bcf86cd799439021", "text": "3", "is_correct": false },
    { "id": "507f1f77bcf86cd799439022", "text": "4", "is_correct": true },
    { "id": "507f1f77bcf86cd799439023", "text": "5", "is_correct": false },
    { "id": "507f1f77bcf86cd799439024", "text": "6", "is_correct": false }
  ],
  "created_at": "2024-01-15T10:35:00.123456",
  "updated_at": "2024-01-15T10:35:00.123456"
}
```

---

### 2. Create a MCQ_MULTI Question

**Endpoint:** `POST /admin/quizzes/<quiz_id>/questions`

**Request Body:**

```json
{
  "type": "MCQ_MULTI",
  "text": "Which of the following are Python data types? (Select all that apply)",
  "points": 10,
  "choices": [
    { "text": "int", "is_correct": true },
    { "text": "string", "is_correct": true },
    { "text": "char", "is_correct": false },
    { "text": "list", "is_correct": true },
    { "text": "array", "is_correct": false }
  ]
}
```

**cURL Example:**

```bash
curl -X POST http://localhost:5000/admin/quizzes/507f1f77bcf86cd799439011/questions \
  -H "Content-Type: application/json" \
  -d '{
    "type": "MCQ_MULTI",
    "text": "Which of the following are Python data types? (Select all that apply)",
    "points": 10,
    "choices": [
      {"text": "int", "is_correct": true},
      {"text": "string", "is_correct": true},
      {"text": "char", "is_correct": false},
      {"text": "list", "is_correct": true},
      {"text": "array", "is_correct": false}
    ]
  }'
```

**Response (201 Created):**

```json
{
  "id": "507f1f77bcf86cd799439025",
  "quiz_id": "507f1f77bcf86cd799439011",
  "type": "MCQ_MULTI",
  "text": "Which of the following are Python data types? (Select all that apply)",
  "points": 10,
  "choices": [
    { "id": "507f1f77bcf86cd799439026", "text": "int", "is_correct": true },
    { "id": "507f1f77bcf86cd799439027", "text": "string", "is_correct": true },
    { "id": "507f1f77bcf86cd799439028", "text": "char", "is_correct": false },
    { "id": "507f1f77bcf86cd799439029", "text": "list", "is_correct": true },
    { "id": "507f1f77bcf86cd799439030", "text": "array", "is_correct": false }
  ],
  "created_at": "2024-01-15T10:40:00.123456",
  "updated_at": "2024-01-15T10:40:00.123456"
}
```

---

### 3. Create a TRUE_FALSE Question

**Endpoint:** `POST /admin/quizzes/<quiz_id>/questions`

**Request Body:**

```json
{
  "type": "TRUE_FALSE",
  "text": "Python is a compiled language.",
  "points": 3,
  "choices": [
    { "text": "True", "is_correct": false },
    { "text": "False", "is_correct": true }
  ]
}
```

**cURL Example:**

```bash
curl -X POST http://localhost:5000/admin/quizzes/507f1f77bcf86cd799439011/questions \
  -H "Content-Type: application/json" \
  -d '{
    "type": "TRUE_FALSE",
    "text": "Python is a compiled language.",
    "points": 3,
    "choices": [
      {"text": "True", "is_correct": false},
      {"text": "False", "is_correct": true}
    ]
  }'
```

**Response (201 Created):**

```json
{
  "id": "507f1f77bcf86cd799439031",
  "quiz_id": "507f1f77bcf86cd799439011",
  "type": "TRUE_FALSE",
  "text": "Python is a compiled language.",
  "points": 3,
  "choices": [
    { "id": "507f1f77bcf86cd799439032", "text": "True", "is_correct": false },
    { "id": "507f1f77bcf86cd799439033", "text": "False", "is_correct": true }
  ],
  "created_at": "2024-01-15T10:45:00.123456",
  "updated_at": "2024-01-15T10:45:00.123456"
}
```

---

### 4. Create a TEXT Question

**Endpoint:** `POST /admin/quizzes/<quiz_id>/questions`

**Request Body:**

```json
{
  "type": "TEXT",
  "text": "What keyword is used to define a function in Python?",
  "points": 5,
  "correct_text": "def"
}
```

**cURL Example:**

```bash
curl -X POST http://localhost:5000/admin/quizzes/507f1f77bcf86cd799439011/questions \
  -H "Content-Type: application/json" \
  -d '{
    "type": "TEXT",
    "text": "What keyword is used to define a function in Python?",
    "points": 5,
    "correct_text": "def"
  }'
```

**Response (201 Created):**

```json
{
  "id": "507f1f77bcf86cd799439034",
  "quiz_id": "507f1f77bcf86cd799439011",
  "type": "TEXT",
  "text": "What keyword is used to define a function in Python?",
  "points": 5,
  "correct_text": "def",
  "choices": [],
  "created_at": "2024-01-15T10:50:00.123456",
  "updated_at": "2024-01-15T10:50:00.123456"
}
```

---

### 5. Update a Question

**Endpoint:** `PUT /admin/questions/<question_id>`

**Request Body:**

```json
{
  "text": "Updated question text",
  "points": 10,
  "choices": [
    { "text": "Option A", "is_correct": true },
    { "text": "Option B", "is_correct": false }
  ]
}
```

**cURL Example:**

```bash
curl -X PUT http://localhost:5000/admin/questions/507f1f77bcf86cd799439020 \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Updated question text",
    "points": 10,
    "choices": [
      {"text": "Option A", "is_correct": true},
      {"text": "Option B", "is_correct": false}
    ]
  }'
```

**Python Example:**

```python
import requests

question_id = "507f1f77bcf86cd799439020"
url = f"http://localhost:5000/admin/questions/{question_id}"

data = {
    "text": "Updated question text",
    "points": 10,
    "choices": [
        {"text": "Option A", "is_correct": True},
        {"text": "Option B", "is_correct": False}
    ]
}

response = requests.put(url, json=data)
print(response.json())
```

**Response (200 OK):**

```json
{
  "id": "507f1f77bcf86cd799439020",
  "quiz_id": "507f1f77bcf86cd799439011",
  "type": "MCQ_SINGLE",
  "text": "Updated question text",
  "points": 10,
  "choices": [
    {
      "id": "507f1f77bcf86cd799439035",
      "text": "Option A",
      "is_correct": true
    },
    {
      "id": "507f1f77bcf86cd799439036",
      "text": "Option B",
      "is_correct": false
    }
  ],
  "created_at": "2024-01-15T10:35:00.123456",
  "updated_at": "2024-01-15T11:00:00.123456"
}
```

---

### 6. Delete a Question

**Endpoint:** `DELETE /admin/questions/<question_id>`

**cURL Example:**

```bash
curl -X DELETE http://localhost:5000/admin/questions/507f1f77bcf86cd799439020
```

**Python Example:**

```python
import requests

question_id = "507f1f77bcf86cd799439020"
url = f"http://localhost:5000/admin/questions/{question_id}"
response = requests.delete(url)
print(response.json())
```

**Response (200 OK):**

```json
{
  "message": "Question deleted successfully"
}
```

---

## Public API

### 1. Get All Published Quizzes

**Endpoint:** `GET /quizzes`

**cURL Example:**

```bash
curl http://localhost:5000/quizzes
```

**Python Example:**

```python
import requests

url = "http://localhost:5000/quizzes"
response = requests.get(url)
quizzes = response.json()
print(quizzes)
```

**Response (200 OK):**

```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "title": "Python Fundamentals Quiz",
    "slug": "python-fundamentals-quiz",
    "description": "Test your knowledge of Python basics",
    "published": true,
    "created_at": "2024-01-15T10:30:00.123456",
    "updated_at": "2024-01-15T10:30:00.123456"
  }
]
```

**Note:** Only quizzes with `published: true` are returned.

---

### 2. Get Quiz by Slug (Without Correct Answers)

**Endpoint:** `GET /quizzes/<slug>`

**cURL Example:**

```bash
curl http://localhost:5000/quizzes/python-fundamentals-quiz
```

**Python Example:**

```python
import requests

slug = "python-fundamentals-quiz"
url = f"http://localhost:5000/quizzes/{slug}"
response = requests.get(url)
quiz = response.json()
print(quiz)
```

**Response (200 OK):**

```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Python Fundamentals Quiz",
  "slug": "python-fundamentals-quiz",
  "description": "Test your knowledge of Python basics",
  "published": true,
  "created_at": "2024-01-15T10:30:00.123456",
  "updated_at": "2024-01-15T10:30:00.123456",
  "questions": [
    {
      "id": "507f1f77bcf86cd799439020",
      "quiz_id": "507f1f77bcf86cd799439011",
      "type": "MCQ_SINGLE",
      "text": "What is the output of print(2 + 2)?",
      "points": 5,
      "choices": [
        { "id": "507f1f77bcf86cd799439021", "text": "3" },
        { "id": "507f1f77bcf86cd799439022", "text": "4" },
        { "id": "507f1f77bcf86cd799439023", "text": "5" },
        { "id": "507f1f77bcf86cd799439024", "text": "6" }
      ],
      "created_at": "2024-01-15T10:35:00.123456",
      "updated_at": "2024-01-15T10:35:00.123456"
    },
    {
      "id": "507f1f77bcf86cd799439025",
      "quiz_id": "507f1f77bcf86cd799439011",
      "type": "MCQ_MULTI",
      "text": "Which of the following are Python data types? (Select all that apply)",
      "points": 10,
      "choices": [
        { "id": "507f1f77bcf86cd799439026", "text": "int" },
        { "id": "507f1f77bcf86cd799439027", "text": "string" },
        { "id": "507f1f77bcf86cd799439028", "text": "char" },
        { "id": "507f1f77bcf86cd799439029", "text": "list" },
        { "id": "507f1f77bcf86cd799439030", "text": "array" }
      ],
      "created_at": "2024-01-15T10:40:00.123456",
      "updated_at": "2024-01-15T10:40:00.123456"
    },
    {
      "id": "507f1f77bcf86cd799439031",
      "quiz_id": "507f1f77bcf86cd799439011",
      "type": "TRUE_FALSE",
      "text": "Python is a compiled language.",
      "points": 3,
      "choices": [
        { "id": "507f1f77bcf86cd799439032", "text": "True" },
        { "id": "507f1f77bcf86cd799439033", "text": "False" }
      ],
      "created_at": "2024-01-15T10:45:00.123456",
      "updated_at": "2024-01-15T10:45:00.123456"
    },
    {
      "id": "507f1f77bcf86cd799439034",
      "quiz_id": "507f1f77bcf86cd799439011",
      "type": "TEXT",
      "text": "What keyword is used to define a function in Python?",
      "points": 5,
      "choices": [],
      "created_at": "2024-01-15T10:50:00.123456",
      "updated_at": "2024-01-15T10:50:00.123456"
    }
  ]
}
```

**Note:** Correct answers (`is_correct`, `correct_text`) are NOT included in the response.

---

### 3. Submit Quiz Attempt

**Endpoint:** `POST /quizzes/<slug>/attempt`

**Request Body:**

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "answers": [
    {
      "question_id": "507f1f77bcf86cd799439020",
      "selected_choice_ids": ["507f1f77bcf86cd799439022"]
    },
    {
      "question_id": "507f1f77bcf86cd799439025",
      "selected_choice_ids": [
        "507f1f77bcf86cd799439026",
        "507f1f77bcf86cd799439027",
        "507f1f77bcf86cd799439029"
      ]
    },
    {
      "question_id": "507f1f77bcf86cd799439031",
      "selected_choice_ids": ["507f1f77bcf86cd799439033"]
    },
    {
      "question_id": "507f1f77bcf86cd799439034",
      "text_answer": "def"
    }
  ]
}
```

**cURL Example:**

```bash
curl -X POST http://localhost:5000/quizzes/python-fundamentals-quiz/attempt \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "answers": [
      {
        "question_id": "507f1f77bcf86cd799439020",
        "selected_choice_ids": ["507f1f77bcf86cd799439022"]
      },
      {
        "question_id": "507f1f77bcf86cd799439025",
        "selected_choice_ids": [
          "507f1f77bcf86cd799439026",
          "507f1f77bcf86cd799439027",
          "507f1f77bcf86cd799439029"
        ]
      },
      {
        "question_id": "507f1f77bcf86cd799439031",
        "selected_choice_ids": ["507f1f77bcf86cd799439033"]
      },
      {
        "question_id": "507f1f77bcf86cd799439034",
        "text_answer": "def"
      }
    ]
  }'
```

**Python Example:**

```python
import requests

slug = "python-fundamentals-quiz"
url = f"http://localhost:5000/quizzes/{slug}/attempt"

data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "answers": [
        {
            "question_id": "507f1f77bcf86cd799439020",
            "selected_choice_ids": ["507f1f77bcf86cd799439022"]
        },
        {
            "question_id": "507f1f77bcf86cd799439025",
            "selected_choice_ids": [
                "507f1f77bcf86cd799439026",
                "507f1f77bcf86cd799439027",
                "507f1f77bcf86cd799439029"
            ]
        },
        {
            "question_id": "507f1f77bcf86cd799439031",
            "selected_choice_ids": ["507f1f77bcf86cd799439033"]
        },
        {
            "question_id": "507f1f77bcf86cd799439034",
            "text_answer": "def"
        }
    ]
}

response = requests.post(url, json=data)
result = response.json()
print(f"Score: {result['score']}/{result['max_score']} ({result['percentage']}%)")
print(result)
```

**Response (201 Created):**

```json
{
  "attempt_id": "507f1f77bcf86cd799439040",
  "quiz_id": "507f1f77bcf86cd799439011",
  "quiz_title": "Python Fundamentals Quiz",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "score": 23,
  "max_score": 23,
  "percentage": 100.0,
  "submitted_at": "2024-01-15T12:00:00.123456",
  "answers": [
    {
      "question_id": "507f1f77bcf86cd799439020",
      "type": "MCQ_SINGLE",
      "is_correct": true,
      "points_awarded": 5,
      "max_points": 5,
      "correct_choice_ids": ["507f1f77bcf86cd799439022"],
      "correct_choice_texts": ["4"]
    },
    {
      "question_id": "507f1f77bcf86cd799439025",
      "type": "MCQ_MULTI",
      "is_correct": true,
      "points_awarded": 10,
      "max_points": 10,
      "correct_choice_ids": [
        "507f1f77bcf86cd799439026",
        "507f1f77bcf86cd799439027",
        "507f1f77bcf86cd799439029"
      ],
      "correct_choice_texts": ["int", "string", "list"]
    },
    {
      "question_id": "507f1f77bcf86cd799439031",
      "type": "TRUE_FALSE",
      "is_correct": true,
      "points_awarded": 3,
      "max_points": 3,
      "correct_choice_ids": ["507f1f77bcf86cd799439033"],
      "correct_choice_texts": ["False"]
    },
    {
      "question_id": "507f1f77bcf86cd799439034",
      "type": "TEXT",
      "is_correct": true,
      "points_awarded": 5,
      "max_points": 5,
      "correct_text": "def"
    }
  ]
}
```

---

## Complete Workflow Example

Here's a complete Python script that demonstrates the full workflow:

```python
import requests
import json

BASE_URL = "http://localhost:5000"

# Step 1: Create a quiz
print("1. Creating a quiz...")
quiz_data = {
    "title": "Python Basics Test",
    "description": "A simple Python quiz",
    "published": True
}
response = requests.post(f"{BASE_URL}/admin/quizzes", json=quiz_data)
quiz = response.json()
quiz_id = quiz["id"]
slug = quiz["slug"]
print(f"   Quiz created: {quiz['title']} (ID: {quiz_id}, Slug: {slug})")

# Step 2: Add questions
print("\n2. Adding questions...")

# Question 1: MCQ_SINGLE
q1_data = {
    "type": "MCQ_SINGLE",
    "text": "What is 2 + 2?",
    "points": 5,
    "choices": [
        {"text": "3", "is_correct": False},
        {"text": "4", "is_correct": True},
        {"text": "5", "is_correct": False}
    ]
}
response = requests.post(f"{BASE_URL}/admin/quizzes/{quiz_id}/questions", json=q1_data)
q1 = response.json()
q1_id = q1["id"]
print(f"   Question 1 created: {q1['text']}")

# Question 2: MCQ_MULTI
q2_data = {
    "type": "MCQ_MULTI",
    "text": "Select all Python data types:",
    "points": 10,
    "choices": [
        {"text": "int", "is_correct": True},
        {"text": "str", "is_correct": True},
        {"text": "char", "is_correct": False},
        {"text": "list", "is_correct": True}
    ]
}
response = requests.post(f"{BASE_URL}/admin/quizzes/{quiz_id}/questions", json=q2_data)
q2 = response.json()
q2_id = q2["id"]
print(f"   Question 2 created: {q2['text']}")

# Question 3: TRUE_FALSE
q3_data = {
    "type": "TRUE_FALSE",
    "text": "Python is an interpreted language.",
    "points": 3,
    "choices": [
        {"text": "True", "is_correct": True},
        {"text": "False", "is_correct": False}
    ]
}
response = requests.post(f"{BASE_URL}/admin/quizzes/{quiz_id}/questions", json=q3_data)
q3 = response.json()
q3_id = q3["id"]
print(f"   Question 3 created: {q3['text']}")

# Question 4: TEXT
q4_data = {
    "type": "TEXT",
    "text": "What keyword defines a function?",
    "points": 5,
    "correct_text": "def"
}
response = requests.post(f"{BASE_URL}/admin/quizzes/{quiz_id}/questions", json=q4_data)
q4 = response.json()
q4_id = q4["id"]
print(f"   Question 4 created: {q4['text']}")

# Step 3: Get published quiz (public API)
print(f"\n3. Fetching quiz by slug: {slug}...")
response = requests.get(f"{BASE_URL}/quizzes/{slug}")
public_quiz = response.json()
print(f"   Quiz: {public_quiz['title']}")
print(f"   Questions: {len(public_quiz['questions'])}")

# Step 4: Submit an attempt
print("\n4. Submitting quiz attempt...")

# Get choice IDs from the public quiz
q1_choices = {c["text"]: c["id"] for c in public_quiz["questions"][0]["choices"]}
q2_choices = {c["text"]: c["id"] for c in public_quiz["questions"][1]["choices"]}
q3_choices = {c["text"]: c["id"] for c in public_quiz["questions"][2]["choices"]}

attempt_data = {
    "name": "Test User",
    "email": "test@example.com",
    "answers": [
        {
            "question_id": q1_id,
            "selected_choice_ids": [q1_choices["4"]]
        },
        {
            "question_id": q2_id,
            "selected_choice_ids": [q2_choices["int"], q2_choices["str"], q2_choices["list"]]
        },
        {
            "question_id": q3_id,
            "selected_choice_ids": [q3_choices["True"]]
        },
        {
            "question_id": q4_id,
            "text_answer": "def"
        }
    ]
}

response = requests.post(f"{BASE_URL}/quizzes/{slug}/attempt", json=attempt_data)
result = response.json()
print(f"   Score: {result['score']}/{result['max_score']} ({result['percentage']}%)")
print(f"   Correct answers: {sum(1 for a in result['answers'] if a['is_correct'])}/{len(result['answers'])}")

# Step 5: Display detailed results
print("\n5. Detailed Results:")
for i, answer in enumerate(result["answers"], 1):
    status = "✓" if answer["is_correct"] else "✗"
    print(f"   Question {i}: {status} ({answer['points_awarded']}/{answer['max_points']} points)")

print("\n✅ Workflow completed!")
```

---

## Error Responses

All endpoints may return error responses in the following format:

**400 Bad Request:**

```json
{
  "error": "Title is required"
}
```

**404 Not Found:**

```json
{
  "error": "Quiz not found"
}
```

**500 Internal Server Error:**

```json
{
  "error": "Internal server error"
}
```

---

## Notes

1. **Question IDs**: When creating questions, choice IDs are auto-generated if not provided
2. **Slug Generation**: Quiz slugs are auto-generated from the title and made unique
3. **Scoring**:
   - MCQ_SINGLE: Full points if correct choice selected
   - MCQ_MULTI: Full points only if exact set of correct choices selected
   - TRUE_FALSE: Full points if correct choice selected
   - TEXT: Full points if answer matches (case-insensitive)
4. **Published Quizzes**: Only quizzes with `published: true` appear in public endpoints
5. **Correct Answers**: Public quiz endpoint does NOT expose correct answers, but attempt submission returns them

---

## Testing with Postman

1. Import the following collection structure:

   - Admin > Quizzes (Create, List, Get, Update, Delete)
   - Admin > Questions (Create, Update, Delete)
   - Public > Quizzes (List, Get by Slug, Submit Attempt)

2. Set base URL variable: `{{base_url}} = http://localhost:5000`

3. Use the request examples above for each endpoint.

---

## JavaScript/Fetch Examples

```javascript
// Get all published quizzes
fetch("http://localhost:5000/quizzes")
  .then((response) => response.json())
  .then((data) => console.log(data));

// Submit quiz attempt
fetch("http://localhost:5000/quizzes/python-fundamentals-quiz/attempt", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    name: "John Doe",
    email: "john@example.com",
    answers: [
      {
        question_id: "507f1f77bcf86cd799439020",
        selected_choice_ids: ["507f1f77bcf86cd799439022"],
      },
    ],
  }),
})
  .then((response) => response.json())
  .then((data) => console.log(data));
```

---

For more information, see the main [README.md](README.md) file.
