from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configure the Flask application
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///fitness_tracker.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    CORS(app)

    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # Import models to ensure they are known to Flask-Migrate
    try:
        from app.models import user, sleep, nutrition, workout
    except ImportError as e:
        print(f"Warning: Could not import models: {e}")

    # Register blueprints
    try:
        from app.routes.main_routes import main_routes
        from app.routes.auth import auth
        
        app.register_blueprint(main_routes)
        app.register_blueprint(auth, url_prefix='/auth')
    except ImportError as e:
        print(f"Warning: Could not import blueprints: {e}")

    return app

# Create the application instance
app = create_app() 