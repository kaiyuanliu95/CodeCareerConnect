from flask import Flask, session, g, jsonify
from flask_login import LoginManager
from models import UserModel, EmailCaptchaModel
import config
from exts import db, mail
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)  # Load configuration from config object

# Initialize extensions
db.init_app(app)  # Initialize SQLAlchemy
mail.init_app(app)  # Initialize Flask-Mail
migrate = Migrate(app, db)  # Enable database migrations

# Setup login manager for handling user sessions
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Specify the login view

# Register blueprints for modularity
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

@login_manager.user_loader
def load_user(user_id):
    """Load the user's ID from the session."""
    return UserModel.query.get(int(user_id))

@app.before_request
def load_logged_in_user():
    """Load user into Flask's global object 'g' if they're logged in."""
    user_id = session.get("user_id")
    if user_id:
        g.user = UserModel.query.get(user_id)
    else:
        g.user = None

@app.context_processor
def inject_user():
    """Inject 'user' variable into the global context for all templates."""
    return {'user': g.user}

if __name__ == '__main__':
    app.run()  # Start the application
