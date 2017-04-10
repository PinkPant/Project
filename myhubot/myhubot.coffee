module.exports = (robot) ->
  convert = require("hubot-myadapter/node_modules/convert-units")

  robot.respond /current time/i, (res) ->
    today = new Date()
    res.send "#{today.getHours()}:#{today.getMinutes()}"

  robot.respond /my tz|my timezone/i, (res) ->
    today = new Date()
    res.send  /\((.*)\)/.exec(today.toString())[1]

  robot.respond /convert$/i, (res) ->
    res.send "Example: 'convert 100 mm to cm'"
    res.send "Available units are: #{convert().possibilities().join(", ")}"

  robot.respond /convert (.*) (.*) to (.*)/i, (res) ->
    value = res.match[1]
    from  = res.match[2]
    to    = res.match[3]

    res.send "#{value} #{from} equals #{convert(value).from(from).to(to)} #{to}"

  robot.respond /user exists (.*)/i, (res) ->
    username = res.match[1]

    robot.http("http://webserver:80/api/user/#{username}")
    .header('Accept', 'application/json')
    .get() (err, HTTPres, body) ->
      res.send "#{username} #{body}"

