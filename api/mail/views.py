from flask import Blueprint, request
from api.models import db, Mail

mail = Blueprint('mail', __name__, url_prefix='/mail')

@mail.route("/register", methods=['POST'])
def register():
  body = request.get_json()
  mail = Mail(email=body['email'], puuid=body['puuid'])
  db.session.add(mail)
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