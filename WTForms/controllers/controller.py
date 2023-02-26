from ..models.model import db, User
from flask import request, render_template, jsonify
from ..forms.login import LoginForm
from ..forms.register import RegisterForm


def method():
    username = request.json["username"]
    password = request.json["password"]
    user = User(
        username=username,
        password=password
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "message": "User created"
    })


def signup_user():
    if request.method == "POST":
        method()
    form = RegisterForm()
    return render_template("register.html", form=form)


def login_user():
    if request.method == "POST":
        method()
    form = LoginForm()
    return render_template("login.html", form=form)
