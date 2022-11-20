from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    puuid = db.Column(db.String, nullable=False)
    
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    skin_id = db.Column(db.String, nullable=False)
    puuid = db.Column(db.String, nullable=False)