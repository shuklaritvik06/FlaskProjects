from flask import Flask, render_template, request
from .config.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from .models.model import db
from .routes.route import auth_manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db.init_app(app)

app.register_blueprint(auth_manager, url_prefix="/")

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def index_page():
    if request.cookies.get("userID"):
        return render_template("index.html")
    return "Please Login/Sign up first!"


if __name__ == "__main__":
    app.run(debug=True)
