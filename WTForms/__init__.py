from flask import Flask
from .config.config import SQLALCHEMY_TRACK_MODIFICATIONS, SQLALCHEMY_DATABASE_URI
from .models.model import db
from .routes.route import wt_manager
from flask_cors import CORS


CORS()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SECRET_KEY"] = "c2d4f2d3e76b8b229ee0f6199437199a"
db.init_app(app)

app.register_blueprint(wt_manager, url_prefix="/v1")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
