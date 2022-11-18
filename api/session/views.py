from flask import Blueprint, request
import cloudscraper
from ..constants import user_agent, base_header

session = Blueprint('session', __name__, url_prefix='/session')

@session.route("/", methods=['POST'])
def index():
  reconnect_ = request.args.get("reconnect", default=False)
  scraper = cloudscraper.create_scraper(browser=user_agent)
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  if reconnect_:
    r = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/session/v1/sessions/{body.get('puuid')}/reconnect", headers=base_header).json()
    return r  
  r = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/session/v1/sessions/{body.get('puuid')}", headers=base_header).json()
  return r
