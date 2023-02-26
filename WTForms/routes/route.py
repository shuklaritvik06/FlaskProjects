from flask import Blueprint
from ..controllers.controller import login_user, signup_user

wt_manager = Blueprint("wt_manager", __name__)

wt_manager.route("/login", methods=["GET", "POST"])(login_user)
wt_manager.route("/signup", methods=["GET", "POST"])(signup_user)
