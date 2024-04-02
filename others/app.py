from flask import Flask, render_template, Blueprint, make_response, jsonify, request

app = Flask(__name__)

bp = Blueprint("bp", __name__)
app.register_blueprint(bp)


@app.before_request
def before_request():
    print("before")


@app.after_request
def after_request(response):
    print("after")
    return response


@app.template_global()
def template_function():
    return "Hi"


@app.template_test()
def is_even(n):
    return n % 2 == 0


@app.route("/")
def handle():
    return render_template("index.html")


@app.route("/res")
def handle_res():
    response = make_response(jsonify({"name": "Rakesh"}))
    response.headers.set("X-Hello", "Hey!")
    return response


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, True)
