from flask import Blueprint, request
from api.utils import scraper
from ..constants import base_header, client_version

party = Blueprint('party', __name__, url_prefix='/party')

@party.route("/party_id")
def party_id():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}",
    "X-Riot-ClientVersion": client_version
  })
  r = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/players/{body.get('puuid')}", headers=base_header).json()
  return r

@party.route("/remove_from_party")
def remove():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}",
  })
  r = scraper.delete(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/players/{body.get('puuid')}", headers=base_header).json()
  return r

@party.route("/info")
def info():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}",
  })
  r = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/{body.get('party_id')}", headers=base_header).json()
  return r
  # todo merge with party_id

@party.route("/set_ready")
def set_ready():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}",
  })
  r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/{body.get('party_id')}/members/{body.get('puuid')}/setReady",json={"ready": body.get('ready')}, headers=base_header).json()
  return r

@party.route("/refresh_tier")
def refresh_tier():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}",
    "X-Riot-ClientVersion": client_version
  })
  r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/{body.get('party_id')}/members/{body.get('puuid')}/refreshCompetitiveTier", headers=base_header).json()
  return r

@party.route("/refresh_identity")
def refresh_identity():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}",
    "X-Riot-ClientVersion": client_version
  })
  r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/{body.get('party_id')}/members/{body.get('puuid')}/refreshPlayerIdentity", headers=base_header).json()
  return r

@party.route("/refresh_ping")
def refresh_ping():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}",
    "X-Riot-ClientVersion": client_version
  })
  r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/{body.get('party_id')}/members/{body.get('puuid')}/refreshPings", headers=base_header).json()
  return r

@party.route("/change_queue")
def change_queue():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}",
  })
  r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/{body.get('party_id')}/queue", json={"queueID": body.get('queue_id')} , headers=base_header).json()
  return r
  # queue id from /info
  
@party.route("/start_custom_game")
def start_custom_game():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}",
    "X-Riot-ClientVersion": client_version
  })
  r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/{body.get('party_id')}/startcustomgame", headers=base_header).json()
  return r

@party.route("/matchmaking_queue")
def matchmaking_queue():
  type_ = request.args.get("type", default="enter")
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}",
  })
  if type_ == "leave":
    r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/{body.get('party_id')}/matchmaking/leave", headers=base_header).json()
    return r
  r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/{body.get('party_id')}/matchmaking/join", headers=base_header).json()
  return r

@party.route("/set_party_accessibility")
def set_party_accessibility():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}",
  })
  r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/{body.get('party_id')}/accessibility", json={"accessibility": body.get('accessibility')} ,headers=base_header).json()
  return r

@party.route("/set_custom_game_settings")
def set_custom_game_settings():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}",
    "X-Riot-ClientVersion": client_version
  })
  payload = {
    "Map": body.get('map'), # content
    "Mode": body.get('mode'), # /info
    "UseBots": body.get('bots'),
    "GamePod": body.get('pod'), # /info
    "GameRules": {
      "AllowGameModifiers": body.get('game_modifier'),
      "PlayOutAllRounds": body.get('play_all_rounds'),
      "SkipMatchHistory": body.get('skip_match_history'),
      "TournamentMode": body.get('tournement_mode'),
      "IsOvertimeWinByTwo": body.get('is_overtime_win_by_two')
    }
  }
  r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/{body.get('party_id')}/customgamesettings", json=payload ,headers=base_header).json()
  return r

@party.route("/invite_by_display_name")
def invite_by_display_name():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}",
    "X-Riot-ClientVersion": client_version
  })
  r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/{body.get('party_id')}/invites/name/{body.get('name')}/tag/{body.get('tag')}", headers=base_header).json()
  return r

@party.route("/request_to_join")
def request_to_join():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}",
  })
  r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/{body.get('party_id')}/request", headers=base_header).json()
  return r

@party.route("/decline_request")
def decline_request():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}",
  })
  r = scraper.post(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/{body.get('party_id')}/request/{body.get('request_id')}/decline", headers=base_header).json()
  return r
  # request_id /info
  
@party.route("/fetch_custom_game_config")
def fetch_custom_game_config():
  body = request.get_json()
  base_header.update({
    "X-Riot-ClientVersion": client_version
  })
  r = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/customgameconfigs", headers=base_header).json()
  return r

@party.route("/tokens")
def tokens():
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}",
  })
  c = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/{body.get('party_id')}/muctoken", headers=base_header).json()
  v = scraper.get(f"https://glz-{body.get('region')}-1.{body.get('region')}.a.pvp.net/parties/v1/parties/{body.get('party_id')}/voicetoken", headers=base_header).json()
  return {
    "chat": c,
    "voice": v
  }