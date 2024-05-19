import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

    # Email configuration
    MAIL_SERVER = "smtp.qq.com"
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = "2849115967@qq.com"
    MAIL_PASSWORD = "uqlbhymhdmrkddgg"
    MAIL_DEFAULT_SENDER = "2849115967@qq.com"

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
     'default': DevelopmentConfig
}
