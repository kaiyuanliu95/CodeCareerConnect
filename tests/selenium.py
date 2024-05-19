import unittest
from flask import session
from app import create_app
from exts import db
from models import UserModel, QuestionModel, AnswerModel
from werkzeug.security import generate_password_hash
from test_data import BasicUnitTests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import threading
import time
import socket

class SeleniumTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create Flask app
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

        # Find a free port and start the Flask server on it
        cls.port = cls.find_free_port()
        cls.server_thread = threading.Thread(target=cls.app.run, kwargs={'port': cls.port, 'debug': False, 'use_reloader': False})
        cls.server_thread.start()
        time.sleep(1)  # Give the server some time to start

        with cls.app.app_context():
            db.create_all()
            cls.test_data = BasicUnitTests()

        # Set up Selenium WebDriver
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)
        cls.driver.get(f'http://localhost:{cls.port}/')

    @classmethod
    def tearDownClass(cls):
        # Stop the Flask server
        cls.driver.quit()
        cls.server_thread.join()

        # Clean up the database
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.user = self.test_data.create_random_user()

    def tearDown(self):
        db.session.rollback()
        db.session.remove()  # Remove the current session to ensure a fresh start
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

    @staticmethod
    def find_free_port():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    def test_login(self):
        try:
            self.driver.get(f'http://localhost:{self.port}/auth/login')
            email_input = self.driver.find_element(By.NAME, 'email')
            password_input = self.driver.find_element(By.NAME, 'password')
            email_input.send_keys(self.user.email)
            password_input.send_keys('password')
            password_input.send_keys(Keys.RETURN)
            time.sleep(1)
            self.assertIn('Welcome', self.driver.page_source)
        except Exception as e:
            print(f"Error in test_login: {e}")
            print(self.driver.page_source)
            raise

    def test_register_user(self):
        try:
            self.driver.get(f'http://localhost:{self.port}/auth/register')
            username_input = self.driver.find_element(By.NAME, 'username')
            email_input = self.driver.find_element(By.NAME, 'email')
            password_input = self.driver.find_element(By.NAME, 'password')
            
            username_input.send_keys('newuser')
            email_input.send_keys('newuser@example.com')
            password_input.send_keys('password')
            password_input.send_keys(Keys.RETURN)
            
            time.sleep(2)  # Increase wait time to ensure the page has time to load
            self.assertIn('Log In', self.driver.page_source)
        except Exception as e:
            print(f"Error in test_register_user: {e}")
            print(self.driver.page_source)
            raise

    def test_post_question(self):
        try:
            self.driver.get(f'http://localhost:{self.port}/auth/login')
            email_input = self.driver.find_element(By.NAME, 'email')
            password_input = self.driver.find_element(By.NAME, 'password')
            email_input.send_keys(self.user.email)
            password_input.send_keys('password')
            password_input.send_keys(Keys.RETURN)
            
            time.sleep(1)
            
            self.driver.get(f'http://localhost:{self.port}/qa/post_question')
            title_input = self.driver.find_element(By.NAME, 'title')
            content_input = self.driver.find_element(By.NAME, 'content')
            
            title_input.send_keys('Test Question Title')
            content_input.send_keys('This is a test question content.')
            content_input.send_keys(Keys.RETURN)
            
            time.sleep(2)  # Increase wait time to ensure the page has time to load
            self.assertIn('Test Question Title', self.driver.page_source)
        except Exception as e:
            print(f"Error in test_post_question: {e}")
            print(self.driver.page_source)
            raise

    def test_post_answer(self):
        try:
            self.driver.get(f'http://localhost:{self.port}/auth/login')
            email_input = self.driver.find_element(By.NAME, 'email')
            password_input = self.driver.find_element(By.NAME, 'password')
            email_input.send_keys(self.user.email)
            password_input.send_keys('password')
            password_input.send_keys(Keys.RETURN)
            
            time.sleep(1)
            
            question = self.test_data.create_random_question(author_id=self.user.id)
            self.driver.get(f'http://localhost:{self.port}/qa/detail/{question.id}')
            time.sleep(1)  # Wait for the page to load
            content_input = self.driver.find_element(By.NAME, 'content')
            
            content_input.send_keys('This is a test answer.')
            content_input.send_keys(Keys.RETURN)
            
            time.sleep(2)  # Increase wait time to ensure the page has time to load
            self.assertIn('This is a test answer.', self.driver.page_source)
        except Exception as e:
            print(f"Error in test_post_answer: {e}")
            print(self.driver.page_source)
            raise

    def test_search_question(self):
        try:
            question = self.test_data.create_random_question(author_id=self.user.id)
            
            self.driver.get(f'http://localhost:{self.port}/')
            search_input = self.driver.find_element(By.NAME, 'q')
            
            search_input.send_keys(question.title.split()[0])
            search_input.send_keys(Keys.RETURN)
            
            time.sleep(1)
            self.assertIn(question.title, self.driver.page_source)
        except Exception as e:
            print(f"Error in test_search_question: {e}")
            print(self.driver.page_source)
            raise

if __name__ == '__main__':
    unittest.main()
