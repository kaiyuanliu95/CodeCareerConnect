from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.security import generate_password_hash
import sqlite3



app = Flask(__name__)



# SQLite数据库连接
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# 创建数据库表
def init_db():
    conn = get_db_connection()
    conn.execute(
        'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL)')
    conn.close()



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']

        # 对密码进行哈希处理
        hashed_password = generate_password_hash(password)

        # 将用户数据插入数据库
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                        (username, email, hashed_password))
            conn.commit()
            return jsonify({'message': '注册成功'})
        except sqlite3.IntegrityError:
            return jsonify({'message': '用户名或邮箱已存在'}), 400
        finally:
            conn.close()

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # 模拟用户验证
        if check_credentials(email, password):
            # 登录成功，重定向到首页
            return redirect(url_for('home'))
        else:
            # 登录失败，显示错误消息
            flash('无效的用户名或密码')
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

def check_credentials(email, password):
    # 这里是用户验证的模拟过程，你可以连接数据库来实现真正的验证
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




if __name__ == '__main__':
    init_db()  # 初始化数据库表
    app.run(debug=True)