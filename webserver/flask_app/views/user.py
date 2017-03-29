from flask import abort, Blueprint, flash, redirect, request, render_template, url_for
from flask_login import current_user, login_required
import os

from flask_app import bcrypt
from flask_app.forms.user import CreateForm, DeleteForm, UpdateForm
from flask_app.models import User

__all__ = [
    # GENERAL USER CAN
    "list",
    # ADMIN USER CAN
    "create",
    "update",
    "delete"
]

blueprint = Blueprint("user", __name__)


@blueprint.route("/list/", methods=["GET"], endpoint="list")
@login_required
def index():
    users = User.all()
    return render_template("user/list.html", obj_list=users)


@blueprint.route("/create/", methods=["GET", "POST"])
@login_required
def create():
    if not current_user.is_admin:
        return redirect(url_for(".list"))
    form = CreateForm(request.form)
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    password=bcrypt.generate_password_hash(form.password.data),
                    superuser=form.superuser.data)
        user.create()
        flash("User successfully created")
        return redirect(url_for(".list"))
    return render_template("user/upsert.html", form=form)


@blueprint.route("/update/<string:name>", methods=["GET", "POST"])
@login_required
def update(name):
    if not current_user.is_admin:
        return redirect(url_for(".list"))
    user = User.get(name) or abort(404)
    form = UpdateForm(request.form, obj=user)
    if form.validate_on_submit():
        user.update(form)
        flash("User successfully updated")
        return redirect(url_for(".list"))
    return render_template("user/upsert.html", form=form)


@blueprint.route("/delete/<string:name>", methods=["GET", "POST"])
@login_required
def delete(name):
    if not current_user.is_admin:
        return redirect(url_for(".list"))
    if name == os.environ["DEFAULT_ADMIN"].split(":")[0]:
        abort(403)
    user = User.get(name) or abort(404)
    form = DeleteForm(request.form, obj=user)
    if form.validate_on_submit():
        user.delete()
        flash("User successfully deleted")
        return redirect(url_for(".list"))
    return render_template("user/delete.html", form=form)

