from flask_login import UserMixin, logout_user, current_user

from flask_app import bcrypt, login_manager, redis_store

__all__ = ["User", "Channel"]


class User(UserMixin):
    """ User model
    Redis keys for User:
        Hash of user data
            users:<Username> -> {'password': 'bcrypt_hash', 'superuser': True}
        Set of all User's channels
            users:<Username>:channels -> {'ChannelName1', 'ChannelName2'}
    """

    prefix = "users"

    def __init__(self, name, password, superuser=False):
        self.name = name
        self.password = password
        self.superuser = superuser if superuser else ""

    @property
    def id(self):
        return self.name

    @property
    def is_admin(self):
        return self.superuser == "True"

    def to_dict(self):
        return {"password": self.password,
                "superuser": self.superuser}

    @classmethod
    def to_obj(cls, user_dict, name):
        return User(name=name, **user_dict)

    def create(self):
        redis_key = "%s:%s" % (self.prefix, self.name)
        redis_store.hmset(redis_key, self.to_dict())

    def update(self, form):
        if self.name != form.name.data:
            self.delete()
            self.name = form.name.data
        if form.password.data:
            self.password = bcrypt.generate_password_hash(form.password.data)
        self.superuser = form.superuser.data
        self.create()

    def delete(self):
        redis_key = "%s:%s" % (self.prefix, self.name)
        user_channels_key = "%s:channels" % redis_key
        redis_store.delete(redis_key, user_channels_key)
        if current_user.name == self.name:
            logout_user()

    @classmethod
    def get(cls, name):
        user = None
        redis_key = "%s:%s" % (cls.prefix, name)
        user_dict = redis_store.hgetall(redis_key)
        if user_dict:
            user = cls.to_obj(user_dict, name)
        return user

    @classmethod
    def all(cls):
        redis_keys = [redis_key
                      for redis_key in redis_store.scan_iter(match="%s*" % cls.prefix)
                      if not redis_key.endswith(":channels")]
        users = []
        for redis_key in redis_keys:
            user_dict = redis_store.hgetall(redis_key)
            name = redis_key.split(":")[1]
            users.append(cls.to_obj(user_dict, name))
        return users

    @property
    def channels(self):
        redis_key = "%s:%s:channels" % (self.prefix, self.name)
        return Channel.all(redis_key)

    def subscribe(self, channel):
        """ User subscribed to Channel
        :param channel: Channel name
        """
        redis_key = "%s:%s:channels" % (self.prefix, self.name)
        redis_store.sadd(redis_key, channel)

    def unsubscribe(self, channel):
        """ User unsubscribed from Channel
        :param channel: Channel name
        """
        redis_key = "%s:%s:channels" % (self.prefix, self.name)
        redis_store.srem(redis_key, channel)


class Channel(object):
    """ Chat Channel model
    Redis keys for chat Channel:
        Set of all created Channels:
            channels -> {'ChannelName1', 'ChannelName2'}
        List of all Channel's messages
            channels:<ChannelName1> -> ['Message1', 'Message2']
    """
    prefix = "channels"

    def __init__(self, name):
        self.name = name

    @classmethod
    def to_obj(cls, channel_dict):
        return Channel(**channel_dict)

    def push(self, msg):
        redis_key = "%s:%s" % (self.prefix, self.name)
        redis_store.rpush(redis_key, msg)

    @property
    def messages(self):
        redis_key = "%s:%s" % (self.prefix, self.name)
        messages = redis_store.lrange(redis_key, 0, -1)
        return messages

    def create(self):
        """ Prefix property as redis key
            Add channel name to redis set
        """
        redis_store.sadd(self.prefix, self.name)

    def delete(self, names=None):
        """ Prefix property as redis key
            Remove channel name from redis set
        """
        if names is None:
            names = [self.name]
        redis_store.srem(self.prefix, *names)
        to_delete = ["%s:%s" % (self.prefix, name) for name in names]
        redis_store.delete(*to_delete)

    @classmethod
    def get(cls, name):
        """ Verify that Channel name exists
        Prefix property as redis key
        :param name: Channel name
        :return: Channel name or None
        """
        is_member = redis_store.sismember(cls.prefix, name)
        return cls.to_obj(dict(name=name)) if is_member else None

    @classmethod
    def all(cls, redis_key=''):
        """ Get set of Channel's names
        Prefix property as redis key
        :param redis_key: Key for channels:<Username>
        :return: set of Channel's names
        """
        if redis_key:
            # REMOVE USER'S MISSING CHANNELS
            to_remove = redis_store.sdiff(redis_key, cls.prefix)
            if to_remove:
                redis_store.srem(redis_key, *to_remove)
        else:
            redis_key = cls.prefix
        name_set = redis_store.smembers(redis_key)
        return name_set


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
