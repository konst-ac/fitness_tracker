from .. import db
from datetime import datetime

class WellnessRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    # Overall wellness metrics
    energy_level = db.Column(db.Integer)  # Scale 1-5
    stress_level = db.Column(db.Integer)  # Scale 1-5
    mood = db.Column(db.String(20))
    
    # Physical wellness
    muscle_soreness = db.Column(db.Integer)  # Scale 1-5
    fatigue_level = db.Column(db.Integer)  # Scale 1-5
    hydration_level = db.Column(db.Integer)  # Scale 1-5
    appetite = db.Column(db.Integer)  # Scale 1-5
    
    # Recovery metrics
    resting_heart_rate = db.Column(db.Integer)
    body_weight = db.Column(db.Float)  # in kg
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<WellnessRecord {self.date}>'

    @property
    def overall_wellness_score(self):
        """Calculate overall wellness score based on various metrics"""
        metrics = [
            self.energy_level,
            6 - self.stress_level,  # Invert stress level (5 becomes 1, 1 becomes 5)
            self.hydration_level,
            6 - self.fatigue_level,  # Invert fatigue level
            self.appetite
        ]
        
        # Only calculate if all metrics are present
        if all(metric is not None for metric in metrics):
            return sum(metrics) / len(metrics)
        return None

    def get_workout_recommendation(self):
        """Generate workout recommendations based on wellness metrics"""
        score = self.overall_wellness_score
        if score is None:
            return "Please complete all wellness metrics for a recommendation"
        
        if score >= 4:
            return "You're feeling great! This is a good day for high-intensity training."
        elif score >= 3:
            return "You're doing well. Moderate intensity workout recommended."
        elif score >= 2:
            return "Consider a light workout or recovery activities today."
        else:
            return "Focus on rest and recovery today. Light stretching recommended." 