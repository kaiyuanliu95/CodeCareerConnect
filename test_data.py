from unittest import TestCase
from werkzeug.security import generate_password_hash
from models import UserModel, QuestionModel, AnswerModel

class BasicUnitTests(TestCase):

    def create_user(self, username="testuser", email="test@example.com", password="password"):
        hashed_password = generate_password_hash(password)
        user = UserModel(username=username, email=email, password=hashed_password)
        return user

    def create_question(self, title="Test Question", content="This is a test question.", user_id=1):
        question = QuestionModel(title=title, content=content, user_id=user_id)
        return question

    def create_answer(self, content="This is a test answer.", question_id=1, user_id=1):
        answer = AnswerModel(content=content, question_id=question_id, user_id=user_id)
        return answer
