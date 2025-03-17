from app import db
from datetime import datetime

class SleepRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    sleep_time = db.Column(db.DateTime, nullable=False)
    wake_time = db.Column(db.DateTime, nullable=False)
    quality = db.Column(db.Integer)  # 1-5 scale
    interruptions = db.Column(db.Integer, default=0)
    deep_sleep_duration = db.Column(db.Float)  # in hours
    rem_sleep_duration = db.Column(db.Float)  # in hours
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def duration(self):
        """Calculate total sleep duration in hours"""
        delta = self.wake_time - self.sleep_time
        return delta.total_seconds() / 3600

    def __repr__(self):
        return f'<SleepRecord {self.date}>' 