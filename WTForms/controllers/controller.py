from ..models.model import db, User
from flask import request, render_template, url_for, redirect, flash
from ..forms.add import RegisterForm


def add_user():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = request.form["username"]
            password = request.form["password"]
            user = User(
                username=username,
                password=password
            )
            db.session.add(user)
            db.session.commit()
        if form.errors != {}:
            for err in form.errors.values():
                flash(f"error: {err}")
        return redirect(url_for("wt_manager.add_user"))
    else:
        return render_template("add.html", form=form)
