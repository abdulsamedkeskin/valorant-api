from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv('fernet_key')
f = Fernet(key)

db = SQLAlchemy()

class Mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    puuid = db.Column(db.String, nullable=False)
    region = db.Column(db.String, nullable=False)
    
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    skin_id = db.Column(db.String, nullable=False)
    puuid = db.Column(db.String, nullable=False)
    region = db.Column(db.String, nullable=False)
    
class Tokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cookies = db.Column(db.String, nullable=False)
    puuid = db.Column(db.String, nullable=False)
    region = db.Column(db.String, nullable=False)
    language = db.Column(db.String, nullable=False)
    access_token = db.Column(db.String, nullable=False)
    entitlement_token = db.Column(db.String, nullable=False)
    def __init__(self,cookies, puuid, region, access_token, entitlement_token, language):
        self.cookies = f.encrypt(bytes(cookies, encoding='utf-8'))
        self.puuid = puuid
        self.region = region
        self.language = language
        self.access_token = f.encrypt(bytes(access_token, encoding='utf-8'))
        self.entitlement_token = f.encrypt(bytes(entitlement_token, encoding='utf-8'))