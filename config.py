#encoding: utf-8
import os

# Database configurations
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Enable debugging mode in the application
DEBUG = True

# Email configuration
MAIL_SERVER = 'smtp.gmail.com'
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = 'codecareerconnect@gmail.com'
MAIL_PASSWORD = 'codecareerconnect5505'
MAIL_DEFAULT_SENDER = 'codecareerconnect@gmail.com'

# Secret key for session management
SECRET_KEY = os.urandom(24)