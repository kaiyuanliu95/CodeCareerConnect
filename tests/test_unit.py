import unittest
from flask import session
from app import create_app
from exts import db
from models import UserModel, QuestionModel, AnswerModel
from werkzeug.security import generate_password_hash
from test_data import BasicUnitTests

class AppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()
            cls.test_data = BasicUnitTests()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.user = self.test_data.create_random_user()

    def tearDown(self):
        db.session.rollback()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()


    def test_login_user(self):
        response = self.client.post('/auth/login', json={
            'email': self.user.email,
            'password': 'password'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        with self.client as c:
            c.post('/auth/login', json={
                'email': self.user.email,
                'password': 'password'
            }, content_type='application/json')
            with c.session_transaction() as sess:
                self.assertTrue('user_id' in sess)

    def test_post_question(self):
        self.client.post('/auth/login', json={
            'email': self.user.email,
            'password': 'password'
        }, content_type='application/json')
        
        response = self.client.post('/qa/post_question', data={
            'title': 'New Question',
            'content': 'This is a new question.'
        }, content_type='application/x-www-form-urlencoded')
        
        self.assertEqual(response.status_code, 302)
        new_question = QuestionModel.query.filter_by(title='New Question').first()
        self.assertIsNotNone(new_question)



    def test_post_answer(self):
        self.client.post('/auth/login', json={
            'email': self.user.email,
            'password': 'password'
        }, content_type='application/json')
        
        question = self.test_data.create_random_question(author_id=self.user.id)
        
        response = self.client.post('/qa/answer/public', data={
            'content': 'This is an answer.',
            'question_id': question.id
        }, content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 302)
        answer = AnswerModel.query.filter_by(question_id=question.id).first()
        self.assertIsNotNone(answer)
        self.assertEqual(answer.content, 'This is an answer.')

    def test_search_questions(self):
        self.client.post('/auth/login', json={
            'email': self.user.email,
            'password': 'password'
        }, content_type='application/json')
        
        question = self.test_data.create_random_question(author_id=self.user.id)
        
        response = self.client.get('/qa/search', query_string={'q': question.title})
        self.assertEqual(response.status_code, 200)
        self.assertIn(question.title.encode(), response.data)
    
    def test_logout_user(self):
        self.client.post('/auth/login', json={
            'email': self.user.email,
            'password': 'password'
        }, content_type='application/json')

        response = self.client.get('/auth/logout')
        self.assertEqual(response.status_code, 302)
        with self.client as c:
            with c.session_transaction() as sess:
                self.assertNotIn('user_id', sess)
    
    def test_about_page(self):
        response = self.client.get('/auth/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About Us', response.data)


    def test_post_answer_without_login(self):
        question = self.test_data.create_random_question(author_id=self.user.id)
        self.client.get('/auth/logout')
        response = self.client.post('/qa/answer/public', data={
            'content': 'This is an answer without login.',
            'question_id': question.id
        }, content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 302)

    def test_post_question_without_login(self):
        self.client.get('/auth.logout')
        response = self.client.post('/qa/post_question', data={
            'title': 'Question Test Without Login',
            'content': 'Content for question test without login.'
        }, content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
