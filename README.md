# AI Powered Learning Management System

An AI-powered Learning Management System (LMS) built using Flask and Google Gemini API.  
The platform enables learners and mentors to manage courses, assignments, and AI-assisted learning efficiently.

---

## Features

### Authentication System
- User Signup & Login
- Role-Based Access Control
- Secure Session Management

### Learner Module
- View Available Courses
- Access Learning Materials
- Track Learning Progress
- Submit Assignments
- AI-Powered Learning Assistance

### Mentor Module
- Upload Courses
- Create & Manage Assignments
- Monitor Learner Progress
- Review Assignment Submissions

### AI Integration
- Integrated with Google Gemini API
- AI-Based Smart Replies
- Intelligent Learning Support

---

## Tech Stack

| Technology | Usage |
|------------|-------|
| Python | Backend Development |
| Flask | Web Framework |
| HTML/CSS | Frontend Design |
| JSON | Data Storage |
| Google Gemini API | AI Integration |

---

## Project Structure

```bash
team_chemical/
│
├── app.py
├── users.json
├── courses.json
├── assignments.json
├── progress.json
│
├── templates/
│   ├── learner_dashboard.html
│   ├── mentor_dashboard.html
│   ├── learning_page.html
│   ├── upload_course.html
│   └── ...
│
├── static/
│   └── style.css
│
├── assets/
├── data/
├── models/
└── requirements.txt
```

---

## Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/Manoj-2107/Project.git
cd Project
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

#### Windows
```bash
venv\Scripts\activate
```

#### Linux / Mac
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install flask google-generativeai
```

---

## Configure Gemini API

Add your Gemini API key inside `app.py`:

```python
genai.configure(api_key="YOUR_API_KEY")
```

---

## Run the Application

```bash
python app.py
```

Open in browser:

```bash
http://127.0.0.1:5000
```

---

## Main Modules

### Authentication
Handles user registration, login, and session management.

### Learner Dashboard
- Course Access
- Progress Tracking
- Assignment Submission
- Learning Resources

### Mentor Dashboard
- Course Upload
- Assignment Management
- Learner Monitoring

### AI Assistant
Provides:
- Smart Responses
- AI Learning Support
- Automated Assistance

---

## Future Enhancements

- MySQL/MongoDB Integration
- Password Hashing & Security
- File Upload System
- Real-Time Chat Support
- Quiz & Certification Module
- Cloud Deployment
- Improved UI/UX

---

## Security Notes

- Never expose API keys publicly.
- Use environment variables for sensitive credentials.
- Implement password encryption before production deployment.

---

## Screens Included

- Login Page
- Signup Page
- Learner Dashboard
- Mentor Dashboard
- Assignment Submission Page
- AI Response Interface

---

## Author

Developed by Manoj Kumar using Flask and Google Gemini AI.

---
