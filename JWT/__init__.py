from flask import Flask
from .config.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from .models.model import db
from .routes.route import jwt_manager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db.init_app(app)

app.register_blueprint(jwt_manager, url_prefix="/")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
