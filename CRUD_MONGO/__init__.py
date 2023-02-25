from flask import Flask, jsonify
from CRUD_MONGO.routes.route import mongo_app
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.register_blueprint(mongo_app, url_prefix="/v1")


@app.route("/")
def get_info():
    return jsonify({
        'info': 'API IS UP! Version 1.0.0'
    })


if __name__ == "__main__":
    app.run(debug=True)
