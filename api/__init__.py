from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from .auth import auth
    from .store import store
    from .game import game
    from .session import session
    from .pre_game import pre_game
    from .party import party
    from .contents import contents
    app.register_blueprint(auth)
    app.register_blueprint(store)
    app.register_blueprint(game)
    app.register_blueprint(session)
    app.register_blueprint(pre_game)
    app.register_blueprint(party)
    app.register_blueprint(contents)
    return app