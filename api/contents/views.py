from flask import Blueprint, request
from api.utils import get_contents

contents = Blueprint('contents', __name__, url_prefix='/contents')

@contents.get("/<content_type>")
def offers(content_type):
  language = request.args.get("language", "en-US")
  for_alert = request.args.get("for_alert")
  contents = get_contents(language=language)
  if for_alert:
    data = []
    for i in contents[0][content_type]:
      if i['assetPath'].split("_PrimaryAsset")[0][-1] == "1":
        data.append(i)
    return data
  return contents[0][content_type]