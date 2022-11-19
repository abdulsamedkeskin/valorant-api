from api import create_app
from threading import Thread

def run():
    create_app().run(host="0.0.0.0", port=8080)
run()