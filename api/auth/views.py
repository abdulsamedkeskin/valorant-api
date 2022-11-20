from flask import Blueprint, request
import cloudscraper
from ..constants import auth_cookies, auth_payload, multifactor_payload, user_agent, base_header
from .utils import parse_accessToken
import jwt, json
from api.models import db, Login, f

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route("/login", methods=['POST', 'PUT'])
def login():
  if request.method == 'PUT':
    scraper = cloudscraper.create_scraper(browser=user_agent)
    body = request.get_json()
    multifactor_payload.update({"code": body.get('code')})
    auth = scraper.put("https://auth.riotgames.com/api/v1/authorization", json=multifactor_payload, cookies=body.get('cookies')).json()
    if auth['type'] == 'error':
      return auth
    id_token, accessToken = parse_accessToken(auth)
    base_header.update({
        "Authorization": f"Bearer {accessToken}",
    })
    entitlement_token = scraper.post("https://entitlements.auth.riotgames.com/api/token/v1", headers=base_header)
    entitlement_token = entitlement_token.json()['entitlements_token']
    user = jwt.decode(accessToken, options={"verify_signature": False})
    user = jwt.decode(accessToken, options={"verify_signature": False})
    account_name = jwt.decode(id_token, options={"verify_signature": False})['acct']
    return {
      "access_token": accessToken,
      "entitlement_token": entitlement_token,
      "puuid": user['sub'],
      "region": user['pp']['c'],
      **account_name,
      "cookies": scraper.cookies.get_dict()
    }
  scraper = cloudscraper.create_scraper(browser=user_agent)
  args = request.get_json()
  cookie_request = scraper.post("https://auth.riotgames.com/api/v1/authorization", json=auth_cookies)
  auth_payload.update({"username": args['username'],"password": args['password']})
  auth = scraper.put("https://auth.riotgames.com/api/v1/authorization", json=auth_payload, cookies=cookie_request.cookies, headers=base_header).json()
  if auth['type'] == "multifactor":
    return {
      "type": "multifactor",
      "email": auth['multifactor']['email'],
      "cookies": scraper.cookies.get_dict()
    }, 200
  id_token, accessToken = parse_accessToken(auth)
  base_header.update({
        "Authorization": f"Bearer {accessToken}",
  })
  entitlement_token = scraper.post("https://entitlements.auth.riotgames.com/api/token/v1", headers=base_header)
  entitlement_token = entitlement_token.json()['entitlements_token']
  user = jwt.decode(accessToken, options={"verify_signature": False})
  account_name = jwt.decode(id_token, options={"verify_signature": False})['acct']
  cookies = scraper.cookies.get_dict()
  response = {
    "access_token": accessToken,
    "entitlement_token": entitlement_token,
    "puuid": user['sub'],
    "region": user['pp']['c'],
    **account_name
  }
  login = Login(cookies=str(cookies),response=str(response))
  db.session.add(login)
  db.session.commit()
  return {
    "cookies": cookies
  }
  
@auth.route("/user", methods=['POST'])
def user():
  body = request.get_json()
  login = Login.query.filter_by(cookies=str(body.get('cookies'))).first()
  response = f.decrypt(bytes(list(login.response))).decode("utf-8").replace("\'", "\"")
  db.session.delete(login)
  db.session.commit()
  return json.loads(response)
  
@auth.route("/refresh", methods=['POST'])
def refresh():
  cookies = request.get_json()['cookies']
  scraper = cloudscraper.create_scraper(browser=user_agent)
  refresh_token = scraper.get("https://auth.riotgames.com/authorize?redirect_uri=https%3A%2F%2Fplayvalorant.com%2Fopt_in&client_id=play-valorant-web-prod&response_type=token%20id_token&nonce=1", allow_redirects=False, cookies=cookies)
  accessToken = refresh_token.text.split("access_token=")[1].split("&amp")[0]
  base_header.update({
        "Authorization": f"Bearer {accessToken}",
  })
  entitlement_token = scraper.post("https://entitlements.auth.riotgames.com/api/token/v1", headers=base_header)
  entitlement_token = entitlement_token.json()['entitlements_token']
  user = jwt.decode(accessToken, options={"verify_signature": False})
  return {
    "access_token": accessToken,
    "entitlement_token": entitlement_token,
    "puuid": user['sub'],
    "region": user['pp']['c'],
    "cookies": scraper.cookies.get_dict()
  }