module.exports = (robot) ->
  convert = require("hubot-myadapter/node_modules/convert-units")

  robot.respond /time/i, (res) ->
    today = new Date()
    res.send "#{today.getHours()}:#{today.getMinutes()}"

  robot.respond /tz/i, /timezone/i, (res) ->
    today = new Date()
    res.send  /\((.*)\)/.exec(today.toString())[1]

  robot.respond /convert/, (res) ->
    res.send "Example: 'convert 100 mm to cm'. Available units are: #{convert().possibilities().join(", ")}"

  robot.respond /convert (.*) (.*) to (.*)/i, (res) ->
    value = res.match[1]
    from  = res.match[2]
    to    = res.match[3]

    @robot.logger.info value, from, to

    if !from
      res.send convert(value).possibilities()
      return
    else if !to
      res.send convert(value).from(from).possibilities()
      return

    res.send "#{value} #{from} equals #{convert(value).from(from).to(to)} #{to}"

  robot.respond /is user (.*) exists?/i, (res) ->
    username = res.match[1]

    robot.http("http://webserver:80/api/user/#{username}")
    .header('Accept', 'application/json')
    .get() (err, HTTPres, body) ->
      res.send "#{username} #{body}"

