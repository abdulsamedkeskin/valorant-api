from flask import Blueprint, request
from api.utils import scraper
from ..constants import base_header

game = Blueprint('game', __name__, url_prefix='/game')

@game.route("/match_id", methods=['POST'])
def match_id():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  r = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/core-game/v1/players/{body.get('puuid')}", headers=base_header).json()
  if r['httpStatus'] == 404:
    return {"message": r['message']}, 404
  return r

@game.route("/match", methods=['POST'])
def match():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  r = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/core-game/v1/matches/{body.get('match_id')}", headers=base_header).json()
  return r
  # todo merge with match_id

@game.route("/loadouts", methods=['POST'])
def loadouts():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  r = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/core-game/v1/matches/{body.get('match_id')}/loadouts", headers=base_header).json()
  return r

@game.route("/tokens", methods=['POST'])
def tokens():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  t = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/core-game/v1/matches/{body.get('match_id')}/teamchatmuctoken", headers=base_header).json()
  a = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/core-game/v1/matches/{body.get('match_id')}/allchatmuctoken", headers=base_header).json()
  return {
    "team": t,
    "all": a
  }

@game.route("/leave", methods=['POST'])
def leave():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/core-game/v1/players/{body.get('puuid')}/disassociate/{body.get('match_id')}", headers=base_header).json()
  return r