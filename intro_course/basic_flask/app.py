import result
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import sqlite3

# Flask - the web application framework used to build the web application
# render_template - renders the HTML template
# request - handles http requests (or input) from the browser (client) to send back to the main.py (server)
# redirect and url_for - used for URL redirection to direct the user to a web page
# session - manages the user information
# flash - used to display messages to the user
# datetime - handles date and time operation
# sqlite3 - used for interacting with the SQLite3 database

# Create a Flask app
app = Flask(__name__)  # this creates an instance of the Flask class
app.config['SECRET_KEY'] = 'kariyukisaroku'  # this sets a secret key for session management(thisisasecretkeyyoucanmakeitwhateveryouwant)

#  Creat a connection to the SQLite3 database
def init_db():  # a function to initialise the database and create the users table if it doesn't exist
    conn = sqlite3.connect('basic_flask.db')  # connects to the database named basic_flask,db
    cursor = conn.cursor()  # creates a cursor object to interact with the database using UQL commands
    # cursor.execute() is used to execute SQL commands
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, age INTEGER NOT NULL)''')
    conn.commit()  # commits the changes to the database
    conn.close()  # closes the connection to the database to free up resources/memory

# Create routes for the web application
@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']  # gets the username from the form
    password = request.form['password']  # gets the password from the form
    age = request.form['age']  # gets the age from the form
    conn = sqlite3.connect('basic_flask.db')  # connects to the database
    cursor = conn.cursor()  # creates a cursor object to interact with the database
    # inserts the user details into the user table
    cursor.execute('INSERT INTO history (username, password, age) VALUES (?, ?, ?)', (username, password, age))
    conn.commit()  # commits the changes to the database
    conn.close()  # closes the connection to the database
    flash('Use registered successfully!', 'success')  # displays a success message to the user
    return redirect(url_for('login'))  # redirects the user to the login page

#  add login route
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('basic_flask.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM history WHERE username = ? AND password = ?', (username, password))
    # ? is a placeholder for the values that will be passed in the execute() function
    # (username, password) are the values that will be passed in the execute() function
    # This is a parameterised query to prevent SQL injection attacks
    user = cursor.fetchone()  # fetches the first row of the result
    conn.close()
    if user:
        session['user'] = user[1]
        print(user)
        session['age'] = user[3]
        return redirect(url_for('welcome'))
    return 'Login Failed'


@app.route('/hello_world')
def hello_world():
    return 'Hello, Year 10!'

@app.route('/welcome')
def welcome():
    if 'user' in session:
        user = session['user']
        age = session['age']
        return render_template('welcome.html', user=user, age=age)
    return redirect(url_for('login'))

# Route for logging out
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    session.pop('age', None)
    return redirect(url_for('login'))

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/calculator', methods=['POST'])
def calculator_post():
    result = None
    num1 = int(request.form['num1'])
    num2 = int(request.form['num2'])

    operation = request.form['operator']
    if operation == '+':
        result = num1 + num2
    elif operation == '-':
        result = num1 - num2
    elif operation == '*':
        result = num1 * num2
    elif operation == '/':
        if num2 != 0:
            result = num1 / num2
        else:
            result = "Error: Division by zero is undefined"
    else:
        result = "Invalid operator"
    if result.is_integer():
        result = int(result)
    return render_template('calculator.html', result=result)

# Main code to run the Flask app and initialise the database
if __name__ == '__main__':
    init_db()  # calls the init_db() function to initialise
    app.run(port=5000, debug=True)
