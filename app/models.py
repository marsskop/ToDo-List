from datetime import datetime
from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, index=True, default=None)
    completed = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'<Task {self.task}>'