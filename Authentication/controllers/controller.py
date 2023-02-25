import datetime

from ..models.model import db, Users
from flask import render_template, request, redirect, url_for, make_response
import bcrypt


def login_user():
    if request.method == "POST" and request.cookies.get("userID") is None:
        password = bytes(request.form["password"], "utf-8")
        user = db.get_or_404(Users, int(request.cookies.get("userID")))
        if bcrypt.checkpw(password, user.password):
            return redirect(url_for("index_page"))
        return render_template("login.html")
    elif request.method == "GET" and request.cookies.get("userID") is None:
        return render_template("login.html")
    return redirect(url_for("index_page"))


def register_user():
    if request.method == "POST" and request.cookies.get("userID") is None:
        password = bytes(request.form["password"], "utf-8")
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        user = Users(
            email=request.form["email"],
            password=hashed.decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        resp = make_response(render_template("index.html"))
        resp.set_cookie('userID', str(user.id))
        return resp
    elif request.method == "GET" and request.cookies.get("userID") is None:
        return render_template("signup.html")
    return redirect(url_for("index_page"))


def logout_user():
    resp = make_response(redirect(url_for("index_page")))
    resp.set_cookie('userID', '', expires=0)
    return resp

