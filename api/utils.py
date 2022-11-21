import requests_cache
from datetime import timedelta
import json
import cloudscraper

session = requests_cache.CachedSession(expire_after=timedelta(days=1))

scraper = cloudscraper.create_scraper(browser={'custom':'RiotClient/60.0.6.4770705.4749685 rso-auth (Windows;10;;Professional, x64)' })

def get_contents(language="en-US"):
    contracts = session.get(f"https://valorant-api.com/v1/contracts?language={language}")
    buddies = session.get(f"https://valorant-api.com/v1/buddies/levels?language={language}")
    bundles = session.get(f"https://valorant-api.com/v1/bundles?language={language}")
    player_cards = session.get(f"https://valorant-api.com/v1/playercards?language={language}")
    player_titles = session.get(f"https://valorant-api.com/v1/playertitles?language={language}")
    skin_levels = session.get(f"https://valorant-api.com/v1/weapons/skinlevels?language={language}")
    skins = session.get(f"https://valorant-api.com/v1/weapons/skins?language={language}")
    characters = session.get(f"https://valorant-api.com/v1/agents?isPlayableCharacter=true&language={language}")
    sprays = session.get(f"https://valorant-api.com/v1/sprays?language={language}")
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
        with open(f'contents_{language}.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps([res], ensure_ascii=False))
        return [res]
    else:
        with open(f'contents_{language}.json', 'r', encoding="utf8") as f:
            return json.loads(f.read())
     