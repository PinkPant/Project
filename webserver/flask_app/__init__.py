from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_redis import FlaskRedis
from flask_socketio import SocketIO

__all__ = ["app", "bcrypt", "login_manager", "redis_store", "socketio"]

# App Instance
app = Flask(__name__)
app.config.from_object("flask_app.config")

# Flask-Extensions
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
redis_store = FlaskRedis(app)
socketio = SocketIO(app)#, message_queue=app.config['RABBITMQ_URL'])


@app.before_first_request
def createsuperuser():
    from flask_app.models import User
    import os
    name, password = os.environ["DEFAULT_ADMIN"].split(":")
    admin = User(name=name,
                 password=bcrypt.generate_password_hash(password),
                 superuser=True)
    admin.create()
    del os

# Register App Blueprints
from flask_app.views import channel, general, user
app.register_blueprint(channel.blueprint, url_prefix="/channel")
app.register_blueprint(general.blueprint)
app.register_blueprint(user.blueprint, url_prefix="/user")

import flask_app.events
