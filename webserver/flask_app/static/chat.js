// REQUIRES: jQuery, socket.io

var Chat = function(URL, io, options) {
    var $textarea = options.textarea,
        $input = options.input,
        data = {room: options.room},
        redirect = options.redirect;
    
    var socket,
        self = this;

    $(document).ready(function() {
        socket = io.connect(URL);

        // User connected to Channel
        socket.on('connect', function() {
            socket.emit('joined', data);
        });

        // User chat status (joined, left, subscribed, unsubscribed)
        socket.on('status', function(data) {
            $textarea.val($textarea.val() + '<' + data.msg + '>\n');
            $textarea.scrollTop($textarea[0].scrollHeight);
        });

        // Get message
        socket.on('message', function(data) {
            $textarea.val($textarea.val() + data.msg + '\n');
            $textarea.scrollTop($textarea[0].scrollHeight);
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
    this.subscribe = function(target) {
        socket.emit('subscribe', data);
        $(target).text('Unsubscribe');
        $(target).attr('onclick', '');
        $(target).click(function() {self.unsubscribe(target)});
        return false;
    };

    // Remove Channel from User's list
    this.unsubscribe = function(target) {
        socket.emit('unsubscribe', data);
        $(target).text('Subscribe');
        $(target).attr('onclick', '');
        $(target).click(function(){self.subscribe(target)});
        return false;
    };

    this.leave_room = function() {
        socket.emit('left', data, function() {
            socket.disconnect();
            window.location.href = redirect;
        });
    }

};
