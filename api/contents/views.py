from flask import Blueprint, request
from api.utils import get_contents

contents = Blueprint('contents', __name__, url_prefix='/contents')

@contents.get("/<content_type>")
def fetch_contents(content_type):
  language = request.args.get("language", "en-US")
  contents = get_contents(language=language)
  return contents[0][content_type]