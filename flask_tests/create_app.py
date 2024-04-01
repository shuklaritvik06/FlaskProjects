from flask import Flask


def handle_hello():
    return ""


def create_app():
    app = Flask(__name__)
    app.get("/")(handle_hello)
    return app
