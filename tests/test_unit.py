
import unittest
from flask import session
from app import create_app
from exts import db
from models import UserModel, QuestionModel
from werkzeug.security import generate_password_hash

class AppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password',
            'confirm_password': 'password'
        }, content_type='application/x-www-form-urlencoded')

    def tearDown(self):
        db.session.remove()

    def test_register_user(self):
        response = self.client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }, content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 302)  # Assuming redirect on success
        new_user = UserModel.query.filter_by(email='newuser@example.com').first()
        self.assertIsNotNone(new_user)

    def test_login_user(self):
        # Create user for login test
        user = UserModel(email='test@example.com', username='testuser', password=generate_password_hash('password'))
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'password'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)  # Assuming JSON response on success
        with self.client as c:
                c.post('/auth/login', json={
                    'email': 'test@example.com',
                    'password': 'password'
                }, content_type='application/json')
                self.assertTrue('user_id' in session)

    def test_post_question(self):
        # Login user first
        self.client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'password'
        }, content_type='application/json')
        
        # Post a new question
        response = self.client.post('/qa/post_question', data={
            'title': 'New Question',
            'content': 'This is a new question.'
        }, content_type='application/x-www-form-urlencoded')
        
        self.assertEqual(response.status_code, 302)  # Assuming redirect on success
        new_question = QuestionModel.query.filter_by(title='New Question').first()
        self.assertIsNotNone(new_question)

if __name__ == '__main__':
    unittest.main()
