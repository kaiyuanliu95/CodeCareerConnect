# tests/unit.py
import unittest
from flask import session
from app import create_app
from exts import db
from models import UserModel, QuestionModel, AnswerModel
from test_data import BasicUnitTests

class AppTests(BasicUnitTests):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        db.session.commit()
        db.drop_all()
        db.create_all()
        self.user = self.create_user()
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def test_register_user(self):
        response = self.client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Assuming redirect on success
        new_user = User.query.filter_by(email='newuser@example.com').first()
        self.assertIsNotNone(new_user)

    def test_login_user(self):
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)  # Assuming redirect on success
        self.assertTrue('user_id' in session)

    def test_post_question(self):
        self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password'
        })
        response = self.client.post('/qa/post_question', data={
            'title': 'New Question',
            'content': 'This is a new question.'
        })
        self.assertEqual(response.status_code, 302)  # Assuming redirect on success
        new_question = QuestionModel.query.filter_by(title='New Question').first()
        self.assertIsNotNone(new_question)

if __name__ == '__main__':
    unittest.main()
