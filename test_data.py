from exts import db
from models import UserModel, QuestionModel, AnswerModel
import random
import string
from werkzeug.security import generate_password_hash

class BasicUnitTests:

    def create_random_user(self):
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        email = f"{username}@example.com"
        password = generate_password_hash('password')
        user = UserModel(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    def create_random_question(self, author_id):
        title = ''.join(random.choices(string.ascii_lowercase + ' ', k=20)).strip().capitalize()
        content = ''.join(random.choices(string.ascii_lowercase + ' ', k=100)).strip().capitalize()
        question = QuestionModel(title=title, content=content, author_id=author_id)
        db.session.add(question)
        db.session.commit()
        return question

    def create_random_answer(self, question_id, author_id):
        content = ''.join(random.choices(string.ascii_lowercase + ' ', k=50)).strip().capitalize()
        answer = AnswerModel(content=content, question_id=question_id, author_id=author_id)
        db.session.add(answer)
        db.session.commit()
        return answer
