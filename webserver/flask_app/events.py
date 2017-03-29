from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from flask_app import socketio
from flask_app.models import Channel


@socketio.on("joined")
def joined(data):
    """ Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    join_room(data["room"])
    emit("status", {"msg": current_user.name + " has entered the channel."}, room=data["room"])


@socketio.on("text")
def text(data):
    """ Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    msg = current_user.name + ":" + data["msg"]
    channel = Channel.get(data["room"])
    channel.push(msg)
    emit("message", {"msg": msg}, room=data["room"])


@socketio.on("left")
def left(data):
    """ Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    leave_room(data["room"])
    emit("status", {"msg": current_user.name + " has left the channel."}, room=data["room"])


@socketio.on("subscribe")
def subscribe(data):
    current_user.subscribe(data["room"])
    emit("status", {"msg": current_user.name + " has subscribed to the channel."}, room=data["room"])


@socketio.on("unsubscribe")
def unsubscribe(data):
    current_user.unsubscribe(data["room"])
    emit("status", {"msg": current_user.name + " has unsubscribed."}, room=data["room"])


@socketio.on_error()
def error_handler(e):
    emit("status", {"msg": "Error: %s" % str(e)})
