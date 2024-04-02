from flask import Flask, render_template

app = Flask(__name__)


app.add_url_rule("/ex", endpoint="example")


@app.endpoint("example")
def example():
    pass


# It allows you to test functions that rely on the request context without actually making an HTTP request.
with app.test_request_context():
    print("Inside test_request_context()")
    from flask import request

    print("Request method:", request.method)

#  It is similar to test_request_context() but is used for creating an application context instead of a request context.
with app.app_context():
    print("Inside app_context()")
    from flask import current_app

    print(current_app.blueprints)
    print("Current app name:", current_app.name)

with app.test_client() as c:
    print("Inside test_client()")
    response = c.get("/")
    print("Response:", response)


# @app.context_processor
# def inject_user():
#     print("Inside context_processor()")
#     return dict(current_user="John Doe")


if __name__ == "__main__":
    app.run(debug=True)
