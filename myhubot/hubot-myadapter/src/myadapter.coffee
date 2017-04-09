try
  {Robot,Adapter,TextMessage,User} = require 'hubot'
catch
  prequire = require('parent-require')
  {Robot,Adapter,TextMessage,User} = prequire 'hubot'

port = parseInt process.env.HUBOT_SOCKETIO_PORT or 5000

io = require('socket.io').listen port

if process.env.HEROKU_URL 
  io.configure ->
    io.set "transports", ["xhr-polling"]
    io.set "polling-duration", 10

class Myadapter extends Adapter

  constructor: ->
    @sockets = {}
    super
    @robot.logger.info "Constructor"

  send: (envelope, strings...) ->
    socket = @sockets[envelope.id]
    socket.emit 'message', str for str in strings
    @robot.logger.info "Send"

  reply: (envelope, strings...) ->
    socket = @sockets[envelope.id]
    for str in strings
      socket.emit 'message', "#{envelope.name}: #{str}"
    @robot.logger.info "Reply"

  run: ->
    io.sockets.on 'connection', (socket) =>
      @sockets[socket.id] = socket

      socket.on 'message', (message) =>
        user = @userForId socket.id, name: 'Try Hubot', room: socket.id
        @receive new TextMessage user, message

      socket.on 'disconnect', =>
        delete @sockets[socket.id]

    @robot.logger.info "Run bot. Listening websocket port #{port}"
    @emit "connected"
    user = new User 1001, name: 'Sample User'
    message = new TextMessage user, 'Some Sample Message', 'MSG-001'
    @robot.receive message


exports.use = (robot) ->
  new Myadapter robot

