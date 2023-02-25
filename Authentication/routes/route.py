from flask import Blueprint
from ..controllers.controller import login_user, register_user, logout_user

auth_manager = Blueprint("auth_manager", __name__)

auth_manager.route("/login", methods=["GET", "POST"])(login_user)
auth_manager.route("/signup", methods=["GET", "POST"])(register_user)
auth_manager.route("/logout", methods=["POST"])(logout_user)
