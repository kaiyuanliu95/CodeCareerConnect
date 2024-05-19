import unittest
from app import create_app
from exts import db
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time

class SeleniumTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up the class...")
        # Create Flask app
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

        # Start Flask server in a separate thread
        cls.server_thread = threading.Thread(target=cls.app.run, kwargs={'debug': False, 'use_reloader': False})
        cls.server_thread.start()
        time.sleep(1)  # Give the server some time to start

        with cls.app.app_context():
            db.create_all()

        # Set up Selenium WebDriver
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)
        print("Class setup complete.")

    @classmethod
    def tearDownClass(cls):
        print("Tearing down the class...")
        # Stop Flask server
        cls.driver.quit()
        cls.server_thread.join()

        # Clean up the database
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
        print("Class teardown complete.")

    def setUp(self):
        print("Setting up the test...")

    def tearDown(self):
        print("Tearing down the test...")

    def test_home_page_loads(self):
        print("Testing if the home page loads...")
        try:
            self.driver.get('http://localhost:5000/')
            self.assertIn('CodeCareerConnect', self.driver.title)
            print("Home page test passed.")
        except Exception as e:
            print(f"Error in home page test: {e}")

    def test_register_page_loads(self):
        print("Testing if the register page loads...")
        try:
            self.driver.get('http://localhost:5000/auth/register')
            self.assertIn('User Registration', self.driver.title)
            print("Register page test passed.")
        except Exception as e:
            print(f"Error in register page test: {e}")

    def test_login_page_loads(self):
        print("Testing if the login page loads...")
        try:
            self.driver.get('http://localhost:5000/auth/login')
            self.assertIn('Login', self.driver.title)
            print("Login page test passed.")
        except Exception as e:
            print(f"Error in login page test: {e}")

if __name__ == '__main__':
    unittest.main()
