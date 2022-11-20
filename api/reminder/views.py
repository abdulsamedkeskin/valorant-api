from flask import Blueprint, request
from api.models import db, Reminder

reminder = Blueprint('reminder', __name__, url_prefix='/reminder')

@reminder.route("/add", methods=['POST'])
def register():
  body = request.get_json()
  mail = Reminder(email=body['email'], puuid=body['puuid'], skin_id=body['skin_id'])
  db.session.add(mail)
  db.session.commit()
  return {
    "status": 200,
    "message": "reminder created"
  }, 200
  
@reminder.route("/delete", methods=['DELETE'])
def unsubscribe():
  body = request.get_json()
  mail = db.one_or_404(db.select(Reminder).filter_by(skin_id=body['skin_id'], email=body['email']))  
  db.session.delete(mail)
  db.session.commit()
  return {
    "status": 200,
    "message": "reminder deleted"
  }, 200