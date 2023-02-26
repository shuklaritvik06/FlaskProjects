from flask import Flask
from .config.config import SQLALCHEMY_TRACK_MODIFICATIONS, SQLALCHEMY_DATABASE_URI
from .models.model import db
from .routes.route import wt_manager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

app.register_blueprint(wt_manager, url_prefix="/")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
    