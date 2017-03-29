from flask import abort, Blueprint, flash, redirect, request, render_template, url_for
from flask_login import current_user, login_required

from flask_app.forms.channel import CreateForm, DeleteForm
from flask_app.models import Channel

__all__ = [
    # GENERAL USER CAN
    "list",
    "chat",
    # ADMIN USER CAN
    "create",
    "update",
    "delete"
]

blueprint = Blueprint("channel", __name__)


@blueprint.route("/list/", methods=["GET"], endpoint="list")
@blueprint.route("/list/<show>", methods=["GET"], endpoint="list")
@login_required
def index(show=False):
    """ Show user"s Channel subscriptions
    :param show: Show all available Channels
    """
    channels = Channel.all() if show == "all" else current_user.channels
    return render_template("channel/list.html", str_set=channels)


@blueprint.route("/create/", methods=["GET", "POST"])
@login_required
def create():
    if not current_user.is_admin:
        return redirect(url_for(".list"))
    form = CreateForm(request.form)
    if form.validate_on_submit():
        channel = Channel(name=form.name.data)
        channel.create()
        flash("Channel successfully created")
        return redirect(url_for(".list", show="all"))
    return render_template("channel/upsert.html", form=form)


@blueprint.route("/delete/<string:name>", methods=["GET", "POST"])
@login_required
def delete(name):
    if not current_user.is_admin:
        return redirect(url_for(".list"))
    channel = Channel.get(name) or abort(404)
    form = DeleteForm(request.form, obj=channel)
    if form.validate_on_submit():
        channel.delete()
        flash("channel successfully deleted")
        return redirect(url_for(".list", show="all"))
    return render_template("channel/delete.html", form=form)


@blueprint.route("/chat/")
@blueprint.route("/chat/<string:channel>")
@login_required
def chat(channel=""):
    channel = Channel.get(channel) or abort(404)
    return render_template("channel/chat.html", obj=channel, messages=channel.messages)
