from flask import Blueprint, request
from api.models import db, Reminder, Tokens, f
from api import f_mail
import json
import requests
from flask_mail import Message

reminder = Blueprint('reminder', __name__, url_prefix='/reminder')

@reminder.route("/add", methods=['POST'])
def register():
  body = request.get_json()
  check_ = Reminder.query.filter_by(email=body['email'], skin_id=body['skin_id'])
  if check_.count() >= 1:
    return {
      "status": 400,
      "message": "reminder already added"
    }, 400
  reminder = Reminder(email=body['email'], puuid=body['puuid'], skin_id=body['skin_id'], region=body['region'])
  db.session.add(reminder)
  db.session.commit()
  return {
    "status": 200,
    "message": "reminder created"
  }, 200
  
@reminder.route("/delete", methods=['DELETE'])
def unsubscribe():
  body = request.get_json()
  mail = Reminder.query.filter_by(email=body['email'], skin_id=body['skin_id'])
  if not mail.count() == 1:
     return {
      "status": 404,
      "message": "reminder not found"
    }, 404
  db.session.delete(mail)
  db.session.commit()
  return {
    "status": 200,
    "message": "reminder deleted"
  }, 200
  
@reminder.route("/get", methods=['POST'])
def get_reminders():
  body = request.get_json()
  reminder = Reminder.query.filter_by(puuid=body['puuid'])
  if not reminder.count() == 1:
     return {
      "status": 404,
      "message": "reminder not found"
    }, 404
  data = [i for i in reminder]
  return {
    "status": 200,
    "data": data
  }, 200
  
@reminder.route("/send", methods=['GET'])
def send():
  tokens = Tokens.query.all()
  for i in tokens:
    reminders = Reminder.query.filter_by(puuid=i.puuid)
    length = reminders.count()
    if length > 1:
      if reminders.first().puuid == i.puuid:
        cookies = f.decrypt(bytes(list(i.cookies))).decode("utf-8").replace("\'", "\"")
        cookies = json.loads(cookies)
        access_token = f.decrypt(bytes(list(i.access_token))).decode("utf-8")
        entitlement_token = f.decrypt(bytes(list(i.entitlement_token))).decode("utf-8")
        region = i.region
        puuid = i.puuid
        payload = {
          "access_token": access_token,
          "entitlement_token": entitlement_token,
          "region": region,
          "puuid": puuid
        }
        r = requests.post(f'{request.url_root}store/current?language={i.language}', json=payload).json()          
        for x in reminders:
          for _ in r:
            if _['type'] == 'single':
              for z in _['data']:
                if z['uuid'] == x.skin_id:      
                  msg = Message(f"Valorant Shop Reminder",sender =('Valorant Daily Store','valorantstore.123@gmail.com'), recipients =[reminders.first().email])
                  msg.body = f"{z['displayName']} in store now"
                  f_mail.send(msg)
                  db.session.delete(reminders.first())
                  db.session.commit()
    elif length == 1:
      if reminders.first().puuid == i.puuid:
        access_token = f.decrypt(bytes(list(i.access_token))).decode("utf-8")
        entitlement_token = f.decrypt(bytes(list(i.entitlement_token))).decode("utf-8")
        region = i.region
        puuid = i.puuid
        payload = {
          "region": region,
          "access_token": access_token,
          "entitlement_token": entitlement_token,
          "puuid": puuid
        }
        r = requests.post(f'{request.url_root}store/current?language={i.language}', json=payload).json()          
        for _ in r:
          if _['type'] == "single":
            for z in _['data']:
              if z['uuid'] == reminders.first().skin_id:      
                msg = Message(f"Valorant Shop Reminder",sender =('Valorant Daily Store','valorantstore.123@gmail.com'), recipients =[reminders.first().email])
                msg.body = f"{z['displayName']} in store now"
                f_mail.send(msg)
                db.session.delete(reminders.first())
                db.session.commit()
                break
    else:
        return {
            "status": 400,
            "name": "BAD_REQUEST",
            "description": "no records"
        }, 400
  return {
    "status": 200
  }, 200