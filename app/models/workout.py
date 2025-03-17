from .. import db
from datetime import datetime

class WorkoutRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    workout_type = db.Column(db.String(50), nullable=False)  # strength, cardio, hiit, yoga, etc.
    exercise_name = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Float)  # in kg
    duration = db.Column(db.Integer)  # in minutes
    intensity = db.Column(db.String(20))  # low, medium, high
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<WorkoutRecord {self.date} - {self.workout_type}>'

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # strength, cardio, flexibility, etc.
    equipment_needed = db.Column(db.String(100))
    difficulty_level = db.Column(db.String(20))
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    
    # For custom user-added exercises
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_custom = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Exercise {self.name}>'

class WorkoutPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration_weeks = db.Column(db.Integer)
    difficulty_level = db.Column(db.String(20))
    goal = db.Column(db.String(50))  # strength, endurance, weight loss, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<WorkoutPlan {self.name}>' 