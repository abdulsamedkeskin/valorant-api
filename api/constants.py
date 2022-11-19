from .utils import session

user_agent = {'custom':'RiotClient/60.0.6.4770705.4749685 rso-auth (Windows;10;;Professional, x64)' }
auth_cookies = {
    "client_id": "play-valorant-web-prod",
    "nonce": "1",
    "redirect_uri": "https://playvalorant.com/opt_in",
    "response_type": "token id_token",
    'scope': 'account openid',
}
auth_payload = {
    "type": "auth",
    "remember": False,
    "language": "tr_TR"
}
multifactor_payload = {
    "type": "multifactor",
    "rememberDevice": False,
}
base_header = {
    "Content-Type": "application/json"
}
client_version = session.get("https://valorant-api.com/v1/version").json()['data']['riotClientVersion']
ItemTypeID = {
    "01bb38e1-da47-4e6a-9b3d-945fe4655707": "characters",
    "f85cb6f7-33e5-4dc8-b609-ec7212301948": "Contracts",
    "d5f120f8-ff8c-4aac-92ea-f2b5acbe9475": "sprays",
    "dd3bf334-87f3-40bd-b043-682a57a8dc3a": "Gun Buddies",
    "3f296c07-64c3-494c-923b-fe692a4fa1bd": "playerCards",
    "e7c63390-eda7-46e0-bb7a-a6abdacd2433": "skins",
    "3ad1b2b2-acdb-4524-852f-954a76ddae0a": "skinLevels",
    "de7caa6b-adf7-4588-bbd1-143831e786c6": "playerTitles"
}