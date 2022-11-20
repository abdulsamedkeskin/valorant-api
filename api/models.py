from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    puuid = db.Column(db.String, nullable=False)