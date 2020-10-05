$(document).ready(function () {
    // If the add-song button clicked, post a request with the data.
    $('#addsong_btn').click(function () {
        $('#success_msg').text("");
        $.post({
            url: '',
            data: {
                url: $('#id_url').val(),
                song_name: $('#id_song_name').val(),
                singer: $('#id_singer').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (msg) {
                $('form')[0].reset();
                if (msg == 'Song Added!') {
                    $('#success_msg').text("Added song successfully");
                } else {
                    $('#success_msg').text("Failed to add song");
                }
            },
        });
    });
});