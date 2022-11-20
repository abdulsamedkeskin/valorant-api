from flask import Blueprint, request, render_template
from api.models import db, Mail, Tokens, f
import json
from flask_mail import Message
from datetime import date
from api import f_mail
import requests

mail = Blueprint('mail', __name__, url_prefix='/mail')

@mail.route("/register", methods=['POST'])
def register():
  body = request.get_json()
  check_ = Mail.query.filter_by(email=body['email']).first()
  if check_:
    return {
      "status": 400,
      "message": "email already registered"
    }, 400
  mail = Mail(email=body['email'], puuid=body['puuid'], region=body['region'])
  db.session.add(mail)
  check_ = Tokens.query.filter_by(puuid=body['puuid']).first()
  if not check_:
    tokens = Tokens(cookies=str(body['cookies']), language=body['language'],puuid=body['puuid'], region=body['region'], access_token=body['access_token'], entitlement_token=body['entitlement_token'])
    db.session.add(tokens)
  db.session.commit()
  return {
    "status": 200,
    "message": "mail registered"
  }, 200
  
@mail.route("/unsubscribe/<email>", methods=['GET'])
def unsubscribe(email):
  mail = db.one_or_404(db.select(Mail).filter_by(email=email),description="Mail is not registered")  
  db.session.delete(mail)
  db.session.commit()
  return {
    "status": 200,
    "message": "unsubscribed"
  }, 200
  
@mail.route("/send", methods=['GET'])
def send():
  mail = Mail.query.all()
  for i in mail:
    tokens = Tokens.query.filter_by(puuid=i.puuid).first()
    cookies = f.decrypt(bytes(list(tokens.cookies))).decode("utf-8").replace("\'", "\"")
    cookies = json.loads(cookies)
    access_token = f.decrypt(bytes(list(tokens.access_token))).decode("utf-8")
    entitlement_token = f.decrypt(bytes(list(tokens.entitlement_token))).decode("utf-8")
    region = tokens.region
    puuid = tokens.puuid
    payload = {
      "cookies": cookies,
      "access_token": access_token,
      "entitlement_token": entitlement_token,
      "region": region,
      "puuid": puuid
    }
    r = requests.post(f'{request.url_root}store/current?language={tokens.language}', json=payload).json()
    today = date.today()
    msg = Message(f"Your Valorant store on {today.strftime('%d/%m/%Y')}",sender =('Valorant Daily Store','valorantstore.123@gmail.com'), recipients =[i.email])
    msg.html = render_template("mail.html",results=r, email=i.email) 
    f_mail.send(msg)
  return {
    "status": 200
  }, 200