from flask import Flask, request, jsonify, send_file
import uuid

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload_file():
    f = request.files["file"]
    filename = f"{uuid.uuid4()}.{f.filename.split('.')[-1]}"
    f.save(f"./uploads/{filename}")
    return jsonify({
        "message": "Uploaded to the destination",
        "filename": filename
    })


@app.route("/file/<filename>")
def read_file(filename):
    return send_file(f"./uploads/{filename}")
