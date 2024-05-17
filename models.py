from exts import db
from datetime import datetime
class UserModel(db.Model):
    __tablename__= "user"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(100),nullable=False, unique=True)
    join_time = db.Column(db.DateTime,default=datetime.now)

    def is_active(self):
        return True  # Assume all users are active, adjust as needed
    def get_id(self):
        return str(self.id)
    def is_authenticated(self):
        return True  # Assume all users are authenticated, adjust as needed
    def is_anonymous(self):
        return False  # Assume no anonymous users, adjust as needed

class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    email = db.Column(db.String(100),nullable = False)
    captcha = db.Column(db.String(100),nullable = False)
    # used = db.Column(db.Boolean,default=False)

class QuestionModel(db.Model):
    __tablename__ ="question"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    #foreign key
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    author = db.relationship(UserModel,backref="questions")


class AnswerModel(db.Model):
    __tablename__="answer"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    #foreign key
    question_id = db.Column(db.Integer,db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    #relation
    question = db.relationship(QuestionModel,backref=db.backref("answers",order_by=create_time.desc()))
    author = db.relationship(UserModel, backref="answers")
