import sqlite3

import requests
from flask import Flask, render_template, request, redirect, url_for, session
from openai import OpenAI
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
# Configure your OpenAI API keyclient = Open AI(api_key=Config.OPENAI_API_KEY)
app.secret_key = 'kurosaki'

# database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user['password'], password):
        session['user'] = user[1]
        print(user)
        session['age'] = user[3]
        return redirect(url_for('home'))
    return 'Login Failed'

@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    age = request.form['age']
    hashed_password = generate_password_hash('your_password', method='sha256')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, age) VALUES (?, ?, ?)', (username, password, age))
    conn.commit()
    conn.close()
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

def query_openai(api_key, prompt):
    headers = {'Authorization':f'Bearer {api_key}'}
    data = {'prompt': prompt, 'max_tokens': 150}
    response = requests.post('https://api.openai.net/v1/search/text', headers=headers, json=data)
    return response.json()

# Configure your OpenAI API key
client = OpenAI(api_key=Config.OPENAI_API_KEY)  # Import openai directly, not OpenAI
# Default route for index.html
@app.route('/')
def index():
    return render_template('index.html')
# Route for chat.html which sends request to the chatbot
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']

    retries = 3
    for i in range(retries):
        try:
            # Call OpenAI API
            response = client.chat.completions.create(model="gpt-3.5-turbo",  # Use the cheaper model if possible
            messages=[
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7)

            chatbot_reply = response.choices[0].message.content.strip()
            return {'message': chatbot_reply}

        except RateLimitError:  # Catch the rate limit error properly
            if i < retries - 1:
                time.sleep(2 ** i)  # Exponential backoff: wait and retry
            else:
                return {'message': "Error: Rate limit exceeded. Please try again later."}

if __name__ == '__main__':
    app.run(debug=True)