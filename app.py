from flask import Flask, render_template, request, jsonify
from werkzeug.security import generate_password_hash
import sqlite3

app = Flask(__name__)


# Connect to SQLite database
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

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert user data into the database
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                        (username, email, hashed_password))
            conn.commit()
            return jsonify({'message': 'Registration successful'})
        except sqlite3.IntegrityError:
            return jsonify({'message': 'Username or email already exists'}), 400
        finally:
            conn.close()

    return render_template('register.html')


if __name__ == '__main__':
    init_db()  # Initialize the database table
    app.run(debug=True)
