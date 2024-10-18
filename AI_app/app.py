import sqlite3
import werkzeug
from click import prompt
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import requests

api_endpoint = 'http://localhost:11434/api/chat'

messages = []

app = Flask(__name__)


# Configure your OpenAI API keyclient = Open AI(api_key=Config.OPENAI_API_KEY)
app.config['SECRET_KEY'] = 'kurosaki'

# database connection of users
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # get the data of id, username, password and age into the database.
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        age INTEGER NOT NULL
                    )''')
    conn.commit()  # commits to the database
    conn.close()  # closes the connection to the database

# database connection of history
def get_db_connection():
    conn = sqlite3.connect('chat.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    # get the data of id, user id, prompt, response into the database.
    cursor.execute('''CREATE TABLE history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username INTEGER,
                        prompt TEXT,
                        response TEXT,
                        FOREIGN KEY (username) REFERENCES history (id)
                    )''')
    conn.commit()  # commits to the database
    conn.close()  # closes the connection to the database

# Create routes for the web application
@app.route('/')
def home():
    return render_template('home.html')

# Route to log in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']  # gets the username from the form
        password = request.form['password']  # gets the password from the form
        conn = sqlite3.connect('database.db')  # connects to the database
        cursor = conn.cursor()  # creates a cursor object to interact with the database
        # check the user details
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()  # check the user details by using the database
        conn.close()  # closes the connection to the database
        # code for hashing password
        if user and check_password_hash:
            session['user'] = user[1]
            print(user)
            session['age'] = user[3]
            return redirect(url_for('chat'))  # redirects the user to the page to select what to do
        return 'Login Failed'  # displays a fail message to the user
    return render_template('login.html')

# Route to register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']  # gets the username from the form
        password = request.form['password']  # gets the password from the form
        age = request.form['age']  # gets the age from the form
        werkzeug.security.generate_password_hash('your_password', method='pbkdf2:sha256')  # hashes the password
        conn = sqlite3.connect('database.db')  # connects to the database
        cursor = conn.cursor()  # creates a cursor object to interact with the database
        # inserts the user details into the user table
        cursor.execute('INSERT INTO users (username, password, age) VALUES (?, ?, ?)', (username, password, age))
        conn.commit()  # commits the changes to the database
        conn.close()  # closes the connection to the database
        flash('User registered successfully!', 'success')  # displays a success message to the user
        return redirect(url_for('login'))  # redirects the user to the login page
    return render_template('register.html')

#  Route to log out
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

#  Route to show the user details and chose AI chatbot
@app.route('/chat')
def chat():
    if 'user' in session:
        user = session['user']
        age = session['age']
        return render_template('chat.html', user=user, age=age)
    return redirect(url_for('llama'))  # redirects the user to the llama page

# Route to chat with Llama3.2
@app.route('/llama', methods=['GET', 'POST'])
def llama():
    if 'user' in session:
        user = session['user']

        # Get user ID from the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (user,))
        user_id = cursor.fetchone()
        if user:
            user_id = user

        # Fetch chat history for the logged-in user
        cursor.execute('SELECT * FROM history WHERE user_id = ?', (user_id,))
        user_id = cursor.fetchall()
        conn.close()

    if request.method == 'POST':
        user_input = request.form['input']
        messages.append({'role': 'user', 'content': user_input})

        data = {
            'model': 'llama3.2',
            'stream': False,
            'messages': messages
        }
        response = requests.post(api_endpoint, json=data)

        if response.status_code == 200:
            response_data = response.json()
            assistant_response = response_data['message']['content']
            messages.append({'role': 'chatbot', 'content': assistant_response})
            # save messages to the database with user id
            conn = sqlite3.connect('chat.db')
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO history (user_id, prompt, response) VALUES (?, ?, ?)',
                (session['user'], user_input, assistant_response)
            )
            conn.commit()
            conn.close()
        else:
            print(f'Error: {response.status_code}')

    return render_template('llama.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
