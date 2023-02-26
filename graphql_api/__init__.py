from ariadne import graphql_sync
from flask import Flask, jsonify, request
from .graph_config.configuration import schema
from .config.constant import SQLALCHEMY_TRACK_MODIFICATIONS, SQLALCHEMY_DATABASE_URI
from .models.model import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)


with app.app_context():
    db.create_all()


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value={"request": request})
    status_code = 200 if success else 400
    return jsonify(result), status_code


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
