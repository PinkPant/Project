// REQUIRES: jQuery, socket.io

var Chat = function(URL, io, options) {
    var $wrapper = options.wrapper,
        $input = options.input,
        data = {room: options.room},
        colors = options.colors,
        redirect = options.redirect;
    
    var socket,
        self = this;

    $(document).ready(function() {
        socket = io.connect(URL);

        // User connected to Channel
        socket.on('connect', function() {
            socket.emit('joined', data);
        });

        // User chat status (joined, left, subscribed, unsubscribed, error)
        socket.on('status', function(data) {
            $wrapper.append($('<p />', {'text': '<' + data.msg + '>', 'class': 'chat-message status'}));
            $wrapper.scrollTop($wrapper[0].scrollHeight);
        });

        // Get message
        socket.on('message', function(data) {
            if (!colors.hasOwnProperty(data.username))
                colors[data.username] = "#"+((1<<24)*Math.random()|0).toString(16);
            var $username = $('<span />', {'text': data.username, 'css': {'color': colors[data.username]}});
            var text = $username[0].outerHTML + ': ' + data.msg;
            $wrapper.append($('<p />', {'html': text, 'class': 'chat-message'}));
            $wrapper.scrollTop($wrapper[0].scrollHeight);
        });

        // Send message
        $input.keypress(function(e) {
            var code = e.keyCode || e.which;
            if (code === 13) {
                data.msg = $input.val();
                $input.val('');
                socket.emit('text', data);
            }
        });
    });

    // Add Channel to User's list
    this.join = function(target) {
        socket.emit('join', data);
        $(target).text('Leave');
        $(target).attr('onclick', '');
        $(target).click(function() {self.leave(target)});
    };

    // Remove Channel from User's list
    this.leave = function(target) {
        socket.emit('leave', data);
        $(target).text('Join');
        $(target).attr('onclick', '');
        $(target).click(function(){self.join(target)});
    };

    this.leave_room = function() {
        socket.emit('left', data, function() {
            socket.disconnect();
            window.location.href = redirect;
        });
    }
};

