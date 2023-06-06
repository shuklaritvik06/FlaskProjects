from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload_file():
    f = request.files["file"]
    f.save(f"./uploads/{f.filename}")
    return jsonify({
        "message": "Uploaded to the destination"
    })
