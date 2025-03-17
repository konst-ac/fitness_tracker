from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Profile information
    height = db.Column(db.Float)  # in cm
    weight = db.Column(db.Float)  # in kg
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    activity_level = db.Column(db.String(20))
    
    # Relationships
    sleep_records = db.relationship('SleepRecord', backref='user', lazy=True)
    nutrition_records = db.relationship('NutritionRecord', backref='user', lazy=True)
    workout_records = db.relationship('WorkoutRecord', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>' 