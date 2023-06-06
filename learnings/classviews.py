from flask.views import MethodView
from flask import render_template, request, jsonify


class ClassBasedView(MethodView):
    init_every_request = False

    def get(self):
        return render_template("class.html")

    def post(self):
        return jsonify({
            "data": request.json["name"]
        })

    def patch(self):
        return jsonify({
            "data": request.json["name"]
        })

    def delete(self):
        return jsonify({
            "data": "Deleted"
        })
