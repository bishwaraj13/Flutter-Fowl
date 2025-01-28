from datetime import datetime
from app import db

class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    score = db.Column(db.Integer, index=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)    
