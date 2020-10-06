$(document).ready(function () {
    // If the add-song button clicked, post a request with the data.
    $('#addsong_btn').click(function () {
        if ($('#id_url').val() && $('#id_song_name').val()) {
            $('#success_msg').text("Adding song..., please wait.");
            $('#addsong_btn').attr('disabled', 'disabled');
            $.post({
                url: '',
                data: {
                    url: $('#id_url').val(),
                    song_name: $('#id_song_name').val(),
                    singer: $('#id_singer').val(),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function (msg) {
                    $('#addsong_btn').removeAttr('disabled');
                    $('form')[0].reset();
                    $('#success_msg').text(msg.split("_")[0]);
                    $('#song_cnt').text(msg.split("_")[1])
                },
            });
        }
    });
});