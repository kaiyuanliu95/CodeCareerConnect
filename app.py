from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import sqlite3

app = Flask(__name__)


# SQLite database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Create database table
def init_db():
    conn = get_db_connection()
    conn.execute(
        'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL)')
    conn.close()


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']

        # Hashing passwords
        hashed_password = generate_password_hash(password)

        # Insert user data into database
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                        (username, email, hashed_password))
            conn.commit()
            return jsonify({'message': 'registration success'})
        except sqlite3.IntegrityError:
            return jsonify({'message': 'Username or email already exists'}), 400
        finally:
            conn.close()

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        password = data['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            return jsonify({'success': True, 'message': 'login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}) 

    return render_template('login.html')


def check_credentials(email, password):
    # Here is the simulation process of user verification. You can connect to the database to achieve real verification.
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cur.fetchone()
    conn.close()
    return user is not None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('aboutUs.html')

@app.route('/search')
def search():
    return "Search functionality coming soon!"

# @app.route('/post')
# def post():
#     question = QuestionModel.query.get(qa_id)
#     return render_template('detail.html',question=question)

if __name__ == '__main__':
    init_db()  # Initialize database table
    app.run(debug=True)


