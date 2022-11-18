import requests_cache
from datetime import timedelta
import json

session = requests_cache.CachedSession(expire_after=timedelta(days=1))


def get_contents():
    contracts = session.get("https://valorant-api.com/v1/contracts")
    buddies = session.get("https://valorant-api.com/v1/buddies/levels")
    bundles = session.get("https://valorant-api.com/v1/bundles")
    player_cards = session.get("https://valorant-api.com/v1/playercards")
    player_titles = session.get("https://valorant-api.com/v1/playertitles")
    skin_levels = session.get("https://valorant-api.com/v1/weapons/skinlevels")
    skins = session.get("https://valorant-api.com/v1/weapons/skins")
    characters = session.get("https://valorant-api.com/v1/agents?isPlayableCharacter=true")
    sprays = session.get("https://valorant-api.com/v1/sprays")
    if not contracts.from_cache or not buddies.from_cache or not bundles.from_cache or not player_cards.from_cache or not player_titles.from_cache or not skin_levels.from_cache or not skins.from_cache or not characters.from_cache or not sprays.from_cache:
        res = {}
        res.update({"Contracts": contracts.json()['data']})
        res.update({"Gun Buddies": buddies.json()['data']})
        res.update({"bundles": bundles.json()['data']})
        res.update({"playerCards": player_cards.json()['data']})
        res.update({"playerTitles": player_titles.json()['data']})
        res.update({"skinLevels": skin_levels.json()['data']})
        res.update({"skins": skins.json()['data']})
        res.update({"characters": characters.json()['data']})
        res.update({"sprays": sprays.json()['data']})
        with open('contents.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps([res], ensure_ascii=False))
        return [res]
    else:
        with open('contents.json', 'r') as f:
            return json.loads(f.read())
     