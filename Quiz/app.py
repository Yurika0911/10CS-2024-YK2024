from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import requests
import html
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yurika'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database for saving user quiz results
class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Function to fetch quiz questions
def fetch_questions(amount=5, category=9, difficulty='easy'):
    url = f"https://opentdb.com/api.php?amount={amount}&category={category}&difficulty={difficulty}&type=multiple"
    response = requests.get(url)
    data = response.json()
    return data['results']

# Route for homepage
@app.route('/')
def home():
    return render_template('home.html')

# Route to set quiz parameters
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        session['amount'] = int(request.form.get('amount'))
        session['category'] = int(request.form.get('category'))
        session['difficulty'] = request.form.get('difficulty')
        return redirect(url_for('start_quiz'))
    return render_template('settings.html')

# Route to start quiz
@app.route('/start')
def start_quiz():
    amount = session.get('amount', 5)
    category = session.get('category', 9)
    difficulty = session.get('difficulty', 'easy')

    # Fetch questions and store them in the session
    session['questions'] = fetch_questions(amount, category, difficulty)
    session['score'] = 0
    session['current_question'] = 0
    return redirect(url_for('quiz'))

# Route to display each quiz question
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'questions' not in session:
        return redirect(url_for('settings'))

    questions = session['questions']
    current_question = session['current_question']
    score = session['score']

    if current_question >= len(questions):
        return redirect(url_for('result'))

    question = questions[current_question]
    options = question['incorrect_answers'] + [question['correct_answer']]
    random.shuffle(options)

    if request.method == 'POST':
        selected_option = request.form.get('option')
        if selected_option == question['correct_answer']:
            session['score'] += 1
        session['current_question'] += 1
        return redirect(url_for('quiz'))

    return render_template('quiz.html', question=html.unescape(question['question']), options=options)

# Route for displaying the quiz result and save it to database
@app.route('/result')
def result():
    score = session.get('score', 0)
    total_questions = len(session.get('questions', []))
    username = session.get('username', 'Anonymous')

    # Save the result to the database
    quiz_result = QuizResult(username=username, score=score, total_questions=total_questions)
    db.session.add(quiz_result)
    db.session.commit()

    return render_template('result.html', score=score, total_questions=total_questions)

# Route to view all quiz results
@app.route('/results')
def results():
    all_results = QuizResult.query.all()
    return render_template('results.html', results=all_results)

if __name__ == '__main__':
    app.run(debug=True)