# This file is used to resolve circular imports in the application
from flask_sqlalchemy import SQLAlchemy  # Importing the SQLAlchemy class to handle database operations
from flask_mail import Mail  # Importing the Mail class to handle email sending operations

db = SQLAlchemy()  # Creating an instance of SQLAlchemy to be used as the database adapter
mail = Mail()  # Creating an instance of Mail to be used for sending emails
