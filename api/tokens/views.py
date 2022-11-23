from flask import Blueprint, request
from api.models import db, Tokens, f, Mail, Reminder
import json
import requests
from api import f_mail
from flask_mail import Message

tokens = Blueprint('tokens', __name__, url_prefix='/tokens')

@tokens.route("/refresh", methods=['GET'])
def refresh():
  tokens = Tokens.query.all()
  for i in tokens:
    cookies = f.decrypt(bytes(list(i.cookies))).decode("utf-8").replace("\'", "\"")
    cookies = json.loads(cookies)
    payload = {
      "cookies": cookies
    }
    r = requests.post(f'{request.url_root}auth/refresh', json=payload).json()  
    if r['status'] == 400:
      email = Mail.query.filter_by(puuid=i.puuid)
      if email.count() == 0:
        email = Reminder.query.filter_by(puuid=i.puuid)
      msg = Message('You need to login again',sender =('Valorant Daily Store','mail.valorantstore@gmail.com'), recipients =[email.first().email])
      # todo link
      msg.html = "<p>use the <a href=''>link</a> to login.</p>" 
      f_mail.send(msg)    
    i.access_token = f.encrypt(bytes(r['access_token'], encoding='utf-8'))
    i.entitlement_token = f.encrypt(bytes(r['entitlement_token'], encoding='utf-8'))
    i.cookies = f.encrypt(bytes(str(r['cookies']), encoding='utf-8'))
    db.session.commit()
  return {
    "status": 200
  }, 200