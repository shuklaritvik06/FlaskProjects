from ..models.model import db, User
from flask import request, render_template, url_for, redirect
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
            return redirect(url_for("wt_manager.add_user"))
        if form.errors != {}:
            return render_template("add.html", form=form, error=form.errors.values())
    else:
        return render_template("add.html", form=form, error=[])
