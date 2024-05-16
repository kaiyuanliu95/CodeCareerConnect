from exts import db
from datetime import datetime
from flask_login import UserMixin

class UserModel(db.Model, UserMixin):
    __tablename__ = 'user_model'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    questions = db.relationship('Question', backref='author', lazy=True)
    answers = db.relationship('Answer', backref='author', lazy=True)

    def is_active(self):
        return True  # Assume all users are active, adjust as needed

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True  # Assume all users are authenticated, adjust as needed

    def is_anonymous(self):
        return False  # Assume no anonymous users, adjust as needed
        
        
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)  # 外键引用

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)

class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha_model'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    code = db.Column(db.String(6), nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)

    def is_expired(self):
        return datetime.utcnow() > self.expiration
