from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    address = db.Column(db.String, nullable=False, unique=True)


with app.app_context():
    db.create_all()


@app.route("/")
def get_users():
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()
    data = []
    for i in users:
        data.append({"user": {"id": i.id, "name": i.name, "address": i.address}})
    return jsonify({"data": data})


@app.route("/create", methods=["POST"])
def create_user():
    user = User(name=request.args["name"], address=request.args["address"])
    db.session.add(user)
    db.session.commit()
    return jsonify(
        {"user": {"id": user.id, "name": user.name, "address": user.address}}
    )


@app.route("/delete/<int:id>", methods=["POST"])
def delete_user(id):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(
        {"user": {"id": user.id, "name": user.name, "address": user.address}}
    )


@app.route("/detail/<int:id>", methods=["GET", "POST"])
def detail_user(id):
    user = db.get_or_404(User, id)
    return jsonify(
        {"user": {"id": user.id, "name": user.name, "address": user.address}}
    )
