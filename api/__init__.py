from flask import Flask
from .config import Config
from .models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    from .auth import auth
    from .store import store
    from .game import game
    from .session import session
    from .pre_game import pre_game
    from .party import party
    from .contents import contents
    from .mail import mail
    app.register_blueprint(auth)
    app.register_blueprint(store)
    app.register_blueprint(game)
    app.register_blueprint(session)
    app.register_blueprint(pre_game)
    app.register_blueprint(party)
    app.register_blueprint(contents)
    app.register_blueprint(mail)
    with app.app_context():
        db.create_all()
    return app