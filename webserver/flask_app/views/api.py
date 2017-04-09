from flask import Blueprint, jsonify

from flask_app.models import User

__all__ = [
    "user"
]

blueprint = Blueprint("api", __name__)


@blueprint.route("/user/<username>", methods=["GET"])
def user(username):
    exists = "Exists" if User.get(username) else "Not Exists"
    return jsonify(exists)

