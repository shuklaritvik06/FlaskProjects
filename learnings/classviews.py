from flask.views import MethodView, View
from flask import render_template, request, jsonify
from flask.signals import request_finished


class ListView(View):
    decorators = []

    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self):
        items = self.model.query.all()
        return render_template(self.template, items=items)


class ClassBasedView(MethodView):
    init_every_request = False

    def get(self):
        return render_template("class.html")

    def post(self):
        return jsonify({"data": request.json["name"]})

    def patch(self):
        return jsonify({"data": request.json["name"]})

    def delete(self):
        return jsonify({"data": "Deleted"})
