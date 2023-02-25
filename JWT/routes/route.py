from flask import Blueprint
from ..controllers.controller import register_user, login_user, delete_user

jwt_manager = Blueprint("", __name__)

jwt_manager.route("/login", methods=["POST"])(login_user)
jwt_manager.route("/signup", methods=["POST"])(register_user)
jwt_manager.route("/delete", methods=["POST"])(delete_user)
