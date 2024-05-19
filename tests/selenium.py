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
import threading
import time

class SeleniumTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create Flask app
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

        # Create and start Flask server in a separate thread
        cls.server_thread = threading.Thread(target=cls.app.run, kwargs={'debug': False, 'use_reloader': False})
        cls.server_thread.start()
        time.sleep(1)  # Give the server some time to start

        with cls.app.app_context():
            db.create_all()
            cls.test_data = BasicUnitTests()

        # Set up Selenium WebDriver
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)
        cls.driver.get('http://localhost:5000/')

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

    def test_example(self):
        # Example test case using Selenium WebDriver
        self.driver.get('http://localhost:5000/auth/login')
        email_input = self.driver.find_element_by_name('email')
        password_input = self.driver.find_element_by_name('password')
        email_input.send_keys(self.user.email)
        password_input.send_keys('password')
        password_input.send_keys(Keys.RETURN)
        time.sleep(1)
        self.assertIn('Welcome', self.driver.page_source)
    
    def test_register_user(self):
        self.driver.get('http://localhost:5000/auth/register')
        username_input = self.driver.find_element_by_name('username')
        email_input = self.driver.find_element_by_name('email')
        password_input = self.driver.find_element_by_name('password')
        confirm_password_input = self.driver.find_element_by_name('confirm_password')
        
        username_input.send_keys('newuser')
        email_input.send_keys('newuser@example.com')
        password_input.send_keys('password')
        confirm_password_input.send_keys('password')
        confirm_password_input.send_keys(Keys.RETURN)
        
        time.sleep(1)
        self.assertIn('Login', self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
