from flask import Flask
from .config import Config
from .models import db
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
from werkzeug.exceptions import HTTPException
import json

f_mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    Migrate(app, db)
    CORS(app)
    f_mail.init_app(app)
    from .auth import auth
    from .store import store
    from .game import game
    from .session import session
    from .pre_game import pre_game
    from .party import party
    from .contents import contents
    from .mail import mail
    from .reminder import reminder
    from .tokens import tokens
    app.register_blueprint(auth)
    app.register_blueprint(store)
    app.register_blueprint(game)
    app.register_blueprint(session)
    app.register_blueprint(pre_game)
    app.register_blueprint(party)
    app.register_blueprint(contents)
    app.register_blueprint(mail)
    app.register_blueprint(reminder)
    app.register_blueprint(tokens)
    
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response
    
    with app.app_context():
        db.create_all()
    return app