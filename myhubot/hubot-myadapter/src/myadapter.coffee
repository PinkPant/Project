try
  {Robot,Adapter,TextMessage,User} = require "hubot"
catch
  prequire = require("parent-require")
  {Robot,Adapter,TextMessage,User} = prequire "hubot"

socket = require("socket.io-client").connect "ws://webserver:80/hubot"

class Myadapter extends Adapter
  constructor: ->
    super

  send: (envelope, answer...) ->
    socket.emit "status", "msg": "Hubot says: #{answer}", "room": envelope.room
    @robot.logger.info "Send #{envelope.room}"

  reply: (envelope, strings...) ->
    for str in strings
      socket.emit "message", "#{envelope.name}: #{str}"
    @robot.logger.info "Reply"

  run: ->
    socket.on "connect", =>
      @robot.logger.info "Connected to socket.io server ID: #{socket.id}"

      socket.on "hubot_text", (data) =>
        @robot.logger.info "Got"
        user = @robot.brain.userForId socket.id, name: "Myhubot", room: data.room
        message = new TextMessage user, data.msg
        @robot.logger.info "#{message}"
        @robot.receive message
      @emit "connected"

exports.use = (robot) ->
  new Myadapter robot

