from flask import abort, Blueprint, redirect, request, url_for
from flask_login import current_user, login_user, logout_user

from flask_app import bcrypt
from flask_app.models import User

__all__ = ["home", "authentication", "logout"]

blueprint = Blueprint("general", __name__)


@blueprint.route("/", methods=["GET"])
def home():
    return "Hello World!\n", 200


@blueprint.route("/auth/", methods=["GET"])
def authentication():
    token = request.headers.get("Authorization", request.args.get("token"))
    if token is not None:
        try:
            name, password = token.split(":")  # raise ValueError on bad request
            user = User.get(name)
            if user is not None:
                if current_user.is_authenticated:
                    logout_user()
                if bcrypt.check_password_hash(user.password, password):
                    login_user(user)
        except ValueError:
            abort(400)
        return redirect(url_for("user.list"))
    abort(401)


@blueprint.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("general.home"))
