from flask import Flask, session, g
from flask_login import LoginManager
from exts import db, mail
from config import Config
from models import UserModel
from blueprints.auth import bp as auth_bp
from blueprints.qa import bp as qa_bp
from flask_migrate import Migrate
#from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from config object

# Initialize extensions
db.init_app(app)  # Initialize SQLAlchemy
db.create_all(app=app)
mail.init_app(app)  # Initialize Flask-Mail
migrate = Migrate(app, db)  # Enable database migrations
#csrf = CSRFProtect(app)  # Enable CSRF protection

# Setup login manager for handling user sessions
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Specify the login view

# Register blueprints for modularity
app.register_blueprint(auth_bp)
app.register_blueprint(qa_bp)

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
    app.run(debug=True)  # Start the application
