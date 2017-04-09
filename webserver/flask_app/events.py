from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from flask_app import socketio
from flask_app.models import Channel


@socketio.on("joined")
def joined(data):
    """ Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = data["room"]
    join_room(room)
    emit("status", {"msg": current_user.name + " has entered the channel."}, room=room)


@socketio.on("text")
def text(data):
    """ Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    msg = data["msg"]
    room = data["room"]
    username = current_user.name
    if msg.startswith("myhubot"):
        emit("hubot_text", data, namespace="/hubot", broadcast=True)
    else:
        channel = Channel.get(room)
        channel.push("%s: %s" % (username, msg))
    emit("message", {"username": username, "msg": msg}, room=room)


@socketio.on("status", namespace="/hubot")
def status(data):
    msg = data["msg"]
    emit("status", {"msg": msg}, room=data["room"], namespace="/")


@socketio.on("left")
def left(data):
    """ Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    leave_room(data["room"])
    emit("status", {"msg": current_user.name + " has left the channel."}, room=data["room"])


@socketio.on("join")
def join(data):
    current_user.subscribe(data["room"])
    emit("status", {"msg": current_user.name + " has joined to the channel."}, room=data["room"])


@socketio.on("leave")
def leave(data):
    current_user.unsubscribe(data["room"])
    emit("status", {"msg": current_user.name + " has leave."}, room=data["room"])


@socketio.on_error()
def error_handler(e):
    emit("status", {"msg": "Error: %s" % str(e)})

