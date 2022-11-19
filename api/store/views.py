from flask import Blueprint, request
import cloudscraper
from ..constants import user_agent, base_header, ItemTypeID
from api.utils import session, get_contents

store = Blueprint('store', __name__, url_prefix='/store')

@store.route("/offers", methods=['POST'])
def offers():
  scraper = cloudscraper.create_scraper(browser=user_agent)
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  r = scraper.get(f"https://pd.{body.get('region')}.a.pvp.net/store/v1/offers/", headers=base_header)
  return r.json()

@store.route("/current", methods=['POST'])
def shop():
  scraper = cloudscraper.create_scraper(browser=user_agent)
  body = request.get_json()
  language = request.args.get("language", "en-US")
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  r = scraper.get(f"https://pd.{body.get('region')}.a.pvp.net/store/v2/storefront/{body.get('puuid')}", headers=base_header)
  r = r.json()
  contents = get_contents(language=language)
  data = []
  data_ = {}
  for i in r['SkinsPanelLayout']['SingleItemOffers']:
    _ = next(item for item in contents[0]['skinLevels'] if item["uuid"] == i)
    data_.update({_['displayName']: _})     
  data.append({"type": "single","remaning_time_in_seconds": r['SkinsPanelLayout']['SingleItemOffersRemainingDurationInSeconds'], "data": data_ }) 
  for i in r['FeaturedBundle']['Bundles']:
    data_ = {}
    data__ = {}
    _ = next(item for item in contents[0]['bundles'] if item["uuid"] == i['DataAssetID'])
    for x in i['Items']:
      if x['Item']['ItemTypeID'] == "e7c63390-eda7-46e0-bb7a-a6abdacd2433":
        type_id = '3ad1b2b2-acdb-4524-852f-954a76ddae0a'
      else:
        type_id = x['Item']['ItemTypeID']
      z = next(item for item in contents[0][ItemTypeID[type_id]] if item["uuid"] == x['Item']['ItemID'])
      z['BasePrice'] = x['BasePrice']
      z['DiscountPercent'] = x['DiscountPercent']
      z['DiscountedPrice'] = x['DiscountedPrice']
      z['IsPromoItem'] = x['IsPromoItem']
      data__.update({z['displayName']: z})
    _['items'] = data__
    data_.update({_['displayName']: _,})
  data.append({"remaning_time_in_seconds": r['FeaturedBundle']['BundleRemainingDurationInSeconds'], "type": "bundle", "data": data_})
  return data

@store.route("/wallet", methods=['POST'])
def wallet():
  scraper = cloudscraper.create_scraper(browser=user_agent)
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  r = scraper.get(f"https://pd.{body.get('region')}.a.pvp.net/store/v1/wallet/{body.get('puuid')}", headers=base_header)
  r = r.json()['Balances']
  r['VP'] = r.pop('85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741')
  r['Radianite'] = r.pop('e59aa87c-4cbf-517a-5983-6e81511be9b7')  
  return r

@store.route("my_skins", methods=['POST'])
def my_skins():
  body = request.get_json()
  language = request.args.get("language", "en-US")
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  r = session.get(f"https://pd.{body.get('region')}.a.pvp.net/store/v1/entitlements/{body.get('puuid')}", headers=base_header)
  r = r.json()
  contents = get_contents(language=language)
  data = []
  for i in r['EntitlementsByTypes']:
    type_ = ItemTypeID[i['ItemTypeID']]
    i['type'] = type_
    del i['ItemTypeID']
    data_ = {}
    if type_ == 'skinLevels':
      type_ = 'skins'
    for _ in i['Entitlements']:
      for x in contents[0][type_]:
        if type_ == 'skins':
          try:
            z = next(item for item in x['chromas'] if item["uuid"] == _['ItemID'])
            data_.update({z['displayName']: z})
          except:
            pass
          try:
            y = next(item for item in x['levels'] if item["uuid"] == _['ItemID'])
            data_.update({y['displayName']: y})
          except:
            pass
        elif _['ItemID'] == x['uuid']:
          data_.update({x['displayName']: x})
    data.append({"type": type_, "data": data_})
  return data