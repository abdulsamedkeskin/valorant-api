from flask import Blueprint, request
import cloudscraper
from ..constants import user_agent, base_header, ItemTypeID, currency
from api.utils import session, get_contents

store = Blueprint('store', __name__, url_prefix='/store')

@store.route("/offers", methods=['POST'])
def offers():
  language = request.args.get("language", "en-US")
  body = request.get_json()
  base_header.update({
    "X-Riot-Entitlements-JWT": body.get('entitlement_token'),
    "Authorization": f"Bearer {body.get('access_token')}"
  })
  r = session.get(f"https://pd.{body.get('region')}.a.pvp.net/store/v1/offers/", headers=base_header)
  r = r.json()
  contents = get_contents(language=language)
  data = []
  for i in r['Offers']:
    for _ in i['Rewards']:
      data_ = []
      if _['ItemTypeID'] == 'ea6fcd2e-8373-4137-b1c0-b458947aa86d':
        type_ = "Radianite"
        data.append({"type": type_,"quantity": _['Quantity']})
        continue
      else:
        type_ = ItemTypeID[_['ItemTypeID']]
        for k, v in i['Cost'].items():
          price = f"{str(v)} {currency[k]}"
        for z in contents[0][type_]:
          if type_ == 'skins':
            try:
              a = next(item for item in z['chromas'] if item["uuid"] == _['ItemID'])
              a['price'] = price
              a['quantity'] = _['Quantity']
              a['start_date'] = i['StartDate']
              data_.append(a)
            except:
              pass
            try:
              y = next(item for item in z['levels'] if item["uuid"] == _['ItemID'])
              y['price'] = price
              y['quantity'] = _['Quantity']
              y['start_date'] = i['StartDate']
              data_.append(y)
            except:
              pass
          if z['uuid'] == _['ItemID']:
            z['price'] = price
            z['quantity'] = _['Quantity']
            z['start_date'] = i['StartDate']
            data_.append(z)
      data.append({"type": type_, "data": data_[0]})
  return data

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
  for i in r['FeaturedBundle']['Bundles']:
    data_ = []
    data__ = []
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
      data__.append(z)
    _['items'] = data__
    data_.append(_)
  data.append({"type": "bundle", "remaning_time_in_seconds": r['FeaturedBundle']['BundleRemainingDurationInSeconds'], "data": data_})
  data_ = []
  for i in r['SkinsPanelLayout']['SingleItemOffers']:
    _ = next(item for item in contents[0]['skinLevels'] if item["uuid"] == i)
    data_.append(_)     
  data.append({"type": "single","remaning_time_in_seconds": r['SkinsPanelLayout']['SingleItemOffersRemainingDurationInSeconds'], "data": data_ }) 
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
  r['Free Agent'] = r.pop('f08d4ae3-939c-4576-ab26-09ce1f23bb37')
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
    data_ = []
    if type_ == 'skinLevels':
      type_ = 'skins'
    for _ in i['Entitlements']:
      for x in contents[0][type_]:
        if type_ == 'skins':
          try:
            z = next(item for item in x['chromas'] if item["uuid"] == _['ItemID'])
            data_.append(z)
          except:
            pass
          try:
            y = next(item for item in x['levels'] if item["uuid"] == _['ItemID'])
            data_.append(y)
          except:
            pass
        elif _['ItemID'] == x['uuid']:
          data_.append(x)
    data.append({"type": type_, "data": data_})
  return data