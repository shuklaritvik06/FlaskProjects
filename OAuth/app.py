from flask import Flask, url_for, render_template, make_response, request, redirect
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v2/userinfo',
    client_kwargs={'scope': 'openid profile email'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs'
)

github = oauth.register(
    name='github',
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    request_token_url=None,
    fetch_token=lambda: None,
    client_kwargs={'scope': 'user'}
)


class User(db.Model):
    user_id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/login")
def login():
    return render_template("login.html")


@app.route('/login/google', methods=["POST"])
def login_google():
    redirect_uri = url_for('authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/login/github', methods=["POST"])
def login_github():
    redirect_uri = url_for('authorize_github', _external=True)
    return github.authorize_redirect(redirect_uri)


@app.route('/authorize/google')
def authorize_google():
    token = google.authorize_access_token()
    if token is None:
        return 'Access denied'
    resp = google.get('userinfo')
    user_info = resp.json()
    if db.session.get(User, user_info["id"]) is None:
        user = User(user_id=user_info["id"], email=user_info["email"], name=user_info["name"],
                    picture=user_info["picture"])
        db.session.add(user)
        db.session.commit()
    resp = make_response(redirect(url_for("dashboard_page")))
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=1)
    resp.set_cookie("user_id", str(user_info["id"]), expires=expire_date, httponly=True)
    return resp


@app.route('/authorize/github')
def authorize_github():
    token = github.authorize_access_token()
    if token is None:
        return 'Access denied: reason={0} error={1}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    response = github.get('user', token=token)
    user_info = response.json()
    if db.session.get(User, user_info["id"]) is None:
        user = User(user_id=user_info["id"], email=user_info["email"], name=user_info["name"],
                    picture=user_info["avatar_url"])
        db.session.add(user)
        db.session.commit()
    resp = make_response(redirect(url_for("dashboard_page")))
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=1)
    resp.set_cookie("user_id", str(user_info["id"]), expires=expire_date, httponly=True)
    return resp


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("login")))
    resp.set_cookie("user_id", "", max_age=0)
    return resp


@app.route("/")
def dashboard_page():
    if request.cookies.get("user_id") is None:
        return redirect(url_for("login"))
    print(request.cookies.get("user_id"))
    data = db.session.get(User, request.cookies.get("user_id"))
    return render_template("dashboard.html", data=data)


if __name__ == '__main__':
    app.run()
