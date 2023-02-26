from flask import Blueprint
from ..controllers.controller import add_user

wt_manager = Blueprint("wt_manager", __name__)

wt_manager.route("/add", methods=["GET", "POST"])(add_user)

