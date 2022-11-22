from flask import Blueprint, request
from ..constants import auth_cookies, auth_payload, multifactor_payload, base_header
from .utils import parse_accessToken
import jwt
from api.utils import scraper
from api.models import Tokens, f, db

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route("/login", methods=['POST', 'PUT'])
def login():
  is_mail = request.args.get("mail", False)
  if request.method == 'PUT':
    body = request.get_json()
    multifactor_payload.update({"code": body.get('code')})
    auth = scraper.put("https://auth.riotgames.com/api/v1/authorization", json=multifactor_payload, cookies=body.get('cookies')).json()
    if auth['type'] == 'error':
      if auth['error'] == "invalid_session_id":
        return {
          "status":400,
          "name": "BAD_REQUEST",
          "description": "This code was invalid. Please try again."
        }, 400
    id_token, accessToken = parse_accessToken(auth)
    base_header.update({
        "Authorization": f"Bearer {accessToken}",
    })
    entitlement_token = scraper.post("https://entitlements.auth.riotgames.com/api/token/v1", headers=base_header)
    entitlement_token = entitlement_token.json()['entitlements_token']
    user = jwt.decode(accessToken, options={"verify_signature": False})
    account_name = jwt.decode(id_token, options={"verify_signature": False})['acct']
    cookies = scraper.cookies.get_dict()
    if is_mail:
      tokens = Tokens.query.filter_by(puuid=user['sub'])
      if tokens.count() != 1:
        return {
          "status": 400,
          "name": "BAD_REQUEST",
          "description": "not found on tokens"
        }, 400
      tokens = tokens.first()
      tokens.access_token = f.encrypt(bytes(accessToken, encoding='utf-8'))
      tokens.entitlement_token = f.encrypt(bytes(entitlement_token, encoding='utf-8'))
      tokens.cookies = f.encrypt(bytes(str(cookies), encoding='utf-8'))
      db.session.commit()
      return {
        "status": 200,
        "message": "login successful"
      }, 200
    return {
      "status": 200,
      "access_token": accessToken,
      "entitlement_token": entitlement_token,
      "puuid": user['sub'],
      "region": user['pp']['c'],
      **account_name,
      "cookies": cookies
    }
  args = request.get_json()
  cookie_request = scraper.post("https://auth.riotgames.com/api/v1/authorization", json=auth_cookies)
  auth_payload.update({"username": args['username'],"password": args['password']})
  auth = scraper.put("https://auth.riotgames.com/api/v1/authorization", json=auth_payload, cookies=cookie_request.cookies, headers=base_header).json()
  if auth['type'] == "multifactor":
    return {
      "status": 200,
      "type": "multifactor",
      "email": auth['multifactor']['email'],
      "cookies": scraper.cookies.get_dict()
    }, 200
  try:
    id_token, accessToken = parse_accessToken(auth)
    base_header.update({
          "Authorization": f"Bearer {accessToken}",
    })
    entitlement_token = scraper.post("https://entitlements.auth.riotgames.com/api/token/v1", headers=base_header)
    entitlement_token = entitlement_token.json()['entitlements_token']
    user = jwt.decode(accessToken, options={"verify_signature": False})
    account_name = jwt.decode(id_token, options={"verify_signature": False})['acct']
    cookies = scraper.cookies.get_dict()
    if is_mail:
      tokens = Tokens.query.filter_by(puuid=user['sub'])
      if tokens.count() != 1:
        return {
          "status": 400,
          "name": "BAD_REQUEST",
          "description": "not found on tokens"
        }, 400
      tokens = tokens.first()
      tokens.access_token = f.encrypt(bytes(accessToken, encoding='utf-8'))
      tokens.entitlement_token = f.encrypt(bytes(entitlement_token, encoding='utf-8'))
      tokens.cookies = f.encrypt(bytes(str(cookies), encoding='utf-8'))
      db.session.commit()
      return {
        "status": 200,
        "message": "login successful"
      }, 200
    return {
      "status": 200,
      "cookies": scraper.cookies.get_dict(),
      "access_token": accessToken,
      "entitlement_token": entitlement_token,
      "puuid": user['sub'],
      "region": user['pp']['c'],
      **account_name
    }
  except:
    return {
      "status": 400,
      "name": "BAD_REQUEST",
      "description": "Wrong username or password",
    }, 400
  
@auth.route("/refresh", methods=['POST'])
def refresh():
  try:
    cookies = request.get_json()['cookies']
  except:
    return {
      "status":400,
      "name": "BAD_REQUEST",
      "description": "cookies not found"
    }, 400
  refresh_token = scraper.get("https://auth.riotgames.com/authorize?redirect_uri=https%3A%2F%2Fplayvalorant.com%2Fopt_in&client_id=play-valorant-web-prod&response_type=token%20id_token&nonce=1", allow_redirects=False, cookies=cookies)
  try:
    accessToken = refresh_token.text.split("access_token=")[1].split("&amp")[0]
  except:
    return {
      "status":400,
      "name": "BAD_REQUEST",
      "description": "need to login again"
    }, 400
  base_header.update({
        "Authorization": f"Bearer {accessToken}",
  })
  entitlement_token = scraper.post("https://entitlements.auth.riotgames.com/api/token/v1", headers=base_header)
  entitlement_token = entitlement_token.json()['entitlements_token']
  user = jwt.decode(accessToken, options={"verify_signature": False})
  return {
    "status": 200,
    "access_token": accessToken,
    "entitlement_token": entitlement_token,
    "puuid": user['sub'],
    "region": user['pp']['c'],
    "cookies": scraper.cookies.get_dict()
  }, 200