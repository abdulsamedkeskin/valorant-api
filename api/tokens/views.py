from flask import Blueprint, request
from api.models import db, Tokens, f
import json
import grequests

tokens = Blueprint('tokens', __name__, url_prefix='/tokens')

@tokens.route("/refresh", methods=['GET'])
def register():
  tokens = Tokens.query.all()
  for i in tokens:
    cookies = f.decrypt(bytes(list(i.cookies))).decode("utf-8").replace("\'", "\"")
    cookies = json.loads(cookies)
    payload = {
      "cookies": cookies
    }
    r = grequests.post(f'{request.url_root}auth/refresh', json=payload).json()          
    i.access_token = f.encrypt(bytes(r['access_token'], encoding='utf-8'))
    i.entitlement_token = f.encrypt(bytes(r['entitlement_token'], encoding='utf-8'))
    i.cookies = f.encrypt(bytes(str(r['cookies']), encoding='utf-8'))
    db.session.commit()
  return {
    "status": 200
  }, 200