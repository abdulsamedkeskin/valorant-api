from flask import Blueprint, request
import cloudscraper
from ..constants import user_agent, base_header

pre_game = Blueprint('pre_game', __name__, url_prefix='/pre_game')

@pre_game.route("/match_id", methods=['POST'])
def match_id():
  scraper = cloudscraper.create_scraper(browser=user_agent)
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  r = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/pregame/v1/players/{body.get('puuid')}", headers=base_header).json()
  return r

@pre_game.route("/match", methods=['POST'])
def match():
  scraper = cloudscraper.create_scraper(browser=user_agent)
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  r = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/pregame/v1/matches/{body.get('match_id')}", headers=base_header).json()
  return r
  # todo merge with match_id

@pre_game.route("/loadouts", methods=['POST'])
def loadouts():
  scraper = cloudscraper.create_scraper(browser=user_agent)
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  r = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/pregame/v1/matches/{body.get('match_id')}/loadouts", headers=base_header).json()
  return r

@pre_game.route("/tokens", methods=['POST'])
def tokens():
  scraper = cloudscraper.create_scraper(browser=user_agent)
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  c = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/pregame/v1/matches/{body.get('match_id')}/chattoken", headers=base_header).json()
  v = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/pregame/v1/matches/{body.get('match_id')}/voicetoken", headers=base_header).json()
  return {
    "chat": c,
    "voice": v
  }

@pre_game.route("/select_and_lock", methods=['POST'])
def select_and_lock():  
  scraper = cloudscraper.create_scraper(browser=user_agent)
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/pregame/v1/matches/{body.get('match_id')}/select/{body.get('agent_id')}", headers=base_header).json()
  r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/pregame/v1/matches/{body.get('match_id')}/lock/{body.get('agent_id')}", headers=base_header).json()
  return r


@pre_game.route("/quit", methods=['POST'])
def quit():
  scraper = cloudscraper.create_scraper(browser=user_agent)
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/pregame/v1/matches/{body.get('match_id')}/quit", headers=base_header).json()
  return r