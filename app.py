from api import create_app
from threading import Thread

def run():
    create_app().run(debug=True)
# run()