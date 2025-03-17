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

    # Import models to ensure they are known to Flask-Migrate
    from app.models import user, sleep, nutrition, workout

    # Register blueprints
    try:
        from app.routes import auth, sleep, nutrition, workout
        app.register_blueprint(auth.bp)
        app.register_blueprint(sleep.bp)
        app.register_blueprint(nutrition.bp)
        app.register_blueprint(workout.bp)
    except ImportError as e:
        print(f"Warning: Could not import blueprints: {e}")

    @app.route('/')
    def index():
        return 'Welcome to Fitness Tracker!'

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 