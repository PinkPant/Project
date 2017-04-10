from flask import Blueprint, jsonify

from flask_app.models import User

__all__ = [
    "user"
]

blueprint = Blueprint("api", __name__)


@blueprint.route("/user/<username>", methods=["GET"])
def user(username):
    exists = True if User.get(username) else False
    return jsonify(exists)

