from flask import Flask, session, g, redirect, url_for
from blueprints.auth import bp as auth_bp
from blueprints.qa import bp as qa_bp
import config
from exts import db, mail
from flask_migrate import Migrate
from models import UserModel
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config.config[config_name])  # Load configurations from config object

    db.init_app(app)  # Initialize database with the app
    mail.init_app(app)  # Initialize mail with the app

    migrate = Migrate(app, db)  # Setup database migration

    # Register blueprints for authentication and Q&A functionalities
    app.register_blueprint(qa_bp, url_prefix='/qa')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    login_manager = LoginManager()  # Initialize LoginManager for handling user sessions
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        with app.app_context():
            return UserModel.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('auth.login'))

    @app.before_request
    def my_before_request():
        user_id = session.get("user_id")
        if user_id:
            user = UserModel.query.get(user_id)
            setattr(g, "user", user)
        else:
            setattr(g, "user", None)

    @app.context_processor
    def my_context_processor():
        return {"current_user": current_user}

    @app.route('/')
    def index():
        return redirect(url_for('qa.index'))

    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True)  # Run the Flask application in debug mode
