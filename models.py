from exts import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = "user"  # Name of the table for users in the database
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique ID for each user, auto-incremented
    username = db.Column(db.String(100), nullable=False)  # Username field, must be provided, max length 100 characters
    password = db.Column(db.String(255), nullable=False)  # Password field, must be provided, max length 255 characters
    email = db.Column(db.String(100), nullable=False, unique=True)  # Email field, must be unique and provided
    join_time = db.Column(db.DateTime, default=datetime.now)  # Timestamp of when the user joined, defaults to current time

class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"  # Table to store email captcha for user verification
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique ID for each record, auto-incremented
    email = db.Column(db.String(100), nullable=False)  # Email to which the captcha is sent, must be provided
    captcha = db.Column(db.String(100), nullable=False)  # Captcha code sent to the email, must be provided

class QuestionModel(db.Model):
    __tablename__ = "question"  # Table for storing questions posted by users
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique ID for each question, auto-incremented
    title = db.Column(db.String(100), nullable=False)  # Title of the question, must be provided
    content = db.Column(db.Text, nullable=False)  # Content of the question, must be provided
    create_time = db.Column(db.DateTime, default=datetime.now)  # Timestamp of when the question was created, defaults to current time
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # Foreign key linking to the user who authored the question
    author = db.relationship(UserModel, backref="questions")  # Establishes a relationship between User and Questions, with a back-reference

class AnswerModel(db.Model):
    __tablename__ = "answer"  # Table for storing answers to questions
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique ID for each answer, auto-incremented
    content = db.Column(db.Text, nullable=False)  # Content of the answer, must be provided
    create_time = db.Column(db.DateTime, default=datetime.now)  # Timestamp of when the answer was created, defaults to current time
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))  # Foreign key linking to the question being answered
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # Foreign key linking to the user who authored the answer
    question = db.relationship(QuestionModel, backref=db.backref("answers", order_by=create_time.desc()))  # Relationship to the Question model, organizing answers by most recent
    author = db.relationship(UserModel, backref="answers")  # Establishes a relationship between User and Answers, with a back-reference

