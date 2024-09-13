import sqlite3

import cursor
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'kurosaki'

# database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor.execute('''CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE history(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, prompt TEXT, response TEXT, FOREIGN KEY(user_id)REFERENCES users(id))''')
    conn.commit()
    conn.close()
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

    if user:
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

@app.route('/query_llama3')
def query_llama3(api_key, prompt):
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {'prompt': prompt, 'max_tokens': 150}
    response = request.post('https://api.llama3.com/v1/completions', headers=headers, json=data)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)