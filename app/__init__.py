from flask import Flask
from os import urandom

def create_app(config='CTFd.config'):
    app = Flask(__name__)
    app.secret_key = urandom(24)

    from core import web
    app.register_blueprint(web)

    return app
