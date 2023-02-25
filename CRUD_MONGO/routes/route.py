from flask import Blueprint
from CRUD_MONGO.controllers.controller import get_students, get_student, delete_student, update_student, create_student

mongo_app = Blueprint("mongo_app", __name__)

mongo_app.route('/', methods=['GET'])(get_students)
mongo_app.route('/create', methods=['POST'])(create_student)
mongo_app.route('/update/<int:roll>', methods=['PUT'])(update_student)
mongo_app.route('/delete/<int:roll>', methods=['DELETE'])(delete_student)
mongo_app.route('/get/<int:roll>', methods=['GET'])(get_student)

