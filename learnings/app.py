import os

from flask import Flask, url_for, render_template, request, abort, jsonify, stream_template
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import sentry_sdk
import uuid
from .db import get_db, init_app
from sentry_sdk.integrations.flask import FlaskIntegration
from .classviews import ClassBasedView
from .signals import error_signal

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[
        FlaskIntegration(),
    ],
    traces_sample_rate=1.0
)

app = Flask(__name__)


def handle_forbidden():
    return "You are not allowed buddy!"


app.register_error_handler(400, handle_forbidden)


def get_app():
    return app


app.config.from_mapping(
    SECRET_KEY=f"{uuid.uuid4()}",
    DATABASE="/home/ritvik/FlaskProjects/learnings/db.sqlite",
)


@app.context_processor
def context_adder():
    return dict(data={"favorite": "Paneer"})


class DetailsNotGood(Exception):
    message = "Details are not Okay"

    def to_dict(self):
        return {"message": self.message}


@app.route("/user", methods=["POST", "GET"])
def add_user():
    if request.method == "GET":
        return render_template("user.html")
    if "" in request.form.values():
        error_signal.send(app, error="User provided wrong fields")
        raise DetailsNotGood("Please enter all fields!")
    message = None
    try:
        get_db().execute("INSERT INTO USER VALUES (?,?,?,?)", (request.form["id"], request.form["name"],
                                                               request.form["username"],
                                                               generate_password_hash(request.form["password"])))
        get_db().commit()
        message = "Inserted"
    except get_db().IntegrityError as e:
        message = e
    return jsonify({
        "message": message
    })


@app.errorhandler(DetailsNotGood)
def details_not_good(e):
    return jsonify(e.to_dict())


@app.route("/")
def home_page():
    app.logger.info("Home Page")
    return stream_template("index.html"), 200


@app.route("/about")
def about_page():
    app.logger.info("About Page")
    return "About Page", 200


@app.route("/projects/")
def project_page():
    app.logger.info("Project Page")
    return "Project Page", 200


@app.route("/upload", methods=["POST"])
def file_upload():
    app.logger.info("File Uploading")
    file = request.files["file"]
    if file is None:
        abort(400)
    filename = f"{uuid.uuid4()}.{secure_filename(file.filename).split('.')[-1]}"
    file.save(f"./uploads/{filename}")
    return "Uploaded", 200


@app.errorhandler(404)
def page_not_found(error):
    return "Not Found", 404


@app.template_filter("add")
def add_number(number):
    return 1 + number


app.jinja_env.filters["add"] = add_number
app.add_url_rule("/test", view_func=ClassBasedView.as_view("my_view"))

init_app(app)

with app.test_request_context():
    print(url_for("home_page", next="/about"))

with app.app_context():
    print(get_db())
