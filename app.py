from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "models/gemini-flash-latest"
)

app = Flask(__name__)

app.secret_key = "your_secret_key"

USERS_FILE = 'users.json'# Helper function to load users
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Helper function to save users
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def home():
    return render_template('modern-login-signin-form.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    confirm = request.form.get('confirm')  # Checkbox field

    users = load_users()

    if not confirm:
        flash('You must agree to the Terms of Service and Privacy Policy to sign up!')
        return redirect(url_for('home'))

    if username in users:
        flash('Username already exists! Please choose a different one.')
        return redirect(url_for('home'))
    else:
        users[username] = {
            'email': email,
            'password': password,
            'role': role
        }
        save_users(users)
        flash('Signup successful! You can now login.')
        return redirect(url_for('home'))
    
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    users = load_users()

    if username in users and users[username]["password"] == password:
        session['username'] = username
        role = users[username].get("role")  # SAFELY get role without crash

        if role == "learner":
            session['role'] = role
            return redirect(url_for('learner_dashboard'))
        elif role == "mentor":
            session['role'] = role
            return redirect(url_for('mentor_dashboard'))
        else:
            flash('Role not found for this user! Please signup again.')
            return redirect(url_for('home'))
    else:
        flash('Invalid username or password. Please try again!')
        return redirect(url_for('home'))
    
@app.route('/learner_dashboard')
def learner_dashboard():
    if 'username' in session and session.get('role') == 'learner':
        username = session['username']

        # Load courses
        try:
            with open('courses.json', 'r') as file:
                courses = json.load(file)
        except FileNotFoundError:
            courses = []

        # Load progress
        try:
            with open('progress.json', 'r') as file:
                progress = json.load(file)
        except FileNotFoundError:
            progress = {}

        user_progress = progress.get(username, [])
        
        # ✅ Correct Progress Calculation
        total_courses = len(courses)
        started_courses = len(user_progress)
        if total_courses > 0:
            progress_percentage = int((started_courses / total_courses) * 100)
        else:
            progress_percentage = 0

        return render_template('learner_dashboard.html', username=username, courses=courses, user_progress=user_progress, progress_percentage=progress_percentage)
    else:
        flash('Unauthorized access. Please login as Learner.')
        return redirect(url_for('home'))
@app.route('/learning')
def learning():
    if 'username' in session and session.get('role') == 'learner':
        username = session['username']

        try:
            with open('courses.json', 'r') as file:
                courses = json.load(file)
        except FileNotFoundError:
            courses = []

        try:
            with open('progress.json', 'r') as file:
                progress = json.load(file)
        except FileNotFoundError:
            progress = {}

        try:
            with open('assignments.json', 'r') as file:
                assignments = json.load(file)
        except FileNotFoundError:
            assignments = {}

        user_progress = progress.get(username, [])
        user_assignments = assignments.get(username, [])

        total_courses = len(courses)
        started_courses = len(user_progress)

        progress_percentage = int((started_courses / total_courses) * 100) if total_courses > 0 else 0

        return render_template('learning_page.html', username=username, courses=courses, user_progress=user_progress, user_assignments=user_assignments, progress_percentage=progress_percentage)
    else:
        return redirect(url_for('home'))

@app.route('/mentor_dashboard')
def mentor_dashboard():
    if 'username' in session and session.get('role') == 'mentor':
        return render_template('mentor_dashboard.html', username=session['username'])
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/chatbot', methods=['POST'])
def chatbot_response():

    question = request.form.get('question')

    if question:

        try:

            response = model.generate_content(question)

            ai_reply = response.text

        except Exception as e:

            ai_reply = f"Error: {str(e)}"

        return render_template(
            'ai_reply.html',
            ai_reply=ai_reply
        )

    return redirect(url_for('learning'))


@app.route('/view_learners')
def view_learners():
    if 'username' in session and session.get('role') == 'mentor':
        users = load_users()
        learners = {username: info for username, info in users.items() if info.get('role') == 'learner'}
        return render_template('view_learners.html', learners=learners)
    else:
        flash('Unauthorized access. Please login as Mentor.')
        return redirect(url_for('home'))
    
@app.route('/upload_course', methods=['GET', 'POST'])
def upload_course():
    if 'username' in session and session.get('role') == 'mentor':
        if request.method == 'POST':
            course_title = request.form.get('title')
            course_description = request.form.get('description')

            # Load existing courses
            try:
                with open('courses.json', 'r') as file:
                    courses = json.load(file)
            except FileNotFoundError:
                courses = []

            # Add new course
            courses.append({
                'title': course_title,
                'description': course_description,
                'mentor': session['username']
            })

            # Save back
            with open('courses.json', 'w') as file:
                json.dump(courses, file, indent=4)

            flash('Course uploaded successfully!')
            return redirect(url_for('mentor_dashboard'))

        return render_template('upload_course.html')
    else:
        flash('Unauthorized access. Please login as Mentor.')
        return redirect(url_for('home'))
    
@app.route('/start_course/<int:course_id>', methods=['POST'])
def start_course(course_id):
    if 'username' in session and session.get('role') == 'learner':
        username = session['username']

        # Load existing progress or create new
        try:
            with open('progress.json', 'r') as file:
                progress = json.load(file)
        except FileNotFoundError:
            progress = {}

        # Update learner's progress
        user_progress = progress.get(username, [])
        if course_id not in user_progress:
            user_progress.append(course_id)
        
        progress[username] = user_progress

        with open('progress.json', 'w') as file:
            json.dump(progress, file, indent=4)

        flash('Course started! Happy learning.')
        return redirect(url_for('learner_dashboard'))
    else:
        flash('Unauthorized action. Please login as Learner.')
        return redirect(url_for('home'))

@app.route('/submit_assignment/<int:course_id>', methods=['GET', 'POST'])
def submit_assignment(course_id):
    if 'username' in session and session.get('role') == 'learner':
        username = session['username']

        if request.method == 'POST':
            title = request.form.get('title')
            answer = request.form.get('answer')

            # Load existing assignments
            try:
                with open('assignments.json', 'r') as file:
                    assignments = json.load(file)
            except FileNotFoundError:
                assignments = {}

            user_assignments = assignments.get(username, [])
            user_assignments.append({
                'course_id': course_id,
                'title': title,
                'answer': answer
            })

            assignments[username] = user_assignments

            with open('assignments.json', 'w') as file:
                json.dump(assignments, file, indent=4)

            flash('Assignment submitted successfully!')
            return redirect(url_for('learner_dashboard'))

        # Load course title for form display
        try:
            with open('courses.json', 'r') as file:
                courses = json.load(file)
            course_title = courses[course_id]['title']
        except:
            course_title = "Unknown Course"

        return render_template('submit_assignment.html', course_title=course_title)
    else:
        flash('Unauthorized action.')
        return redirect(url_for('home'))

@app.route('/view_assignments')
def view_assignments():
    if 'username' in session and session.get('role') == 'mentor':
        # Load all assignments
        try:
            with open('assignments.json', 'r') as file:
                assignments = json.load(file)
        except FileNotFoundError:
            assignments = {}

        # Load all courses
        try:
            with open('courses.json', 'r') as file:
                courses = json.load(file)
        except FileNotFoundError:
            courses = []

        return render_template('view_assignments.html', assignments=assignments, courses=courses)
    else:
        flash('Unauthorized access. Please login as Mentor.')
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
