import os
from flask import current_app as app

basedir = basedir = os.path.abspath(os.path.dirname(__file__) + "/..")

class Config:
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    JSON_SORT_KEYS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')