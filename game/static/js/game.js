$(document).ready(function () {
    $('#final_score').hide();
    $('#start_btn, #final_score button').click(function () {
        $('#choices button').css('pointer-events', "none");
        $('#score').text(0);
        $("#choices .button").text('???');
        getQuestion();
        $('#start_area').hide();
        $('#choices').show();
        $('#final_score').hide();
    });
    answer = "";
    btn_clicked();
});

function getQuestion() {
    $.get({
        url: '',
        data: {
            'start': true,
        },
        success: function (msg) {
            if (msg['endGame']) {
                $('#choices').hide();
                $('#final_score').show();
                $('#final_score span').text($('#score').text());
            } else {
                answer = msg['song']['title'];
                $('#audio').attr("src", msg['song']['src']);
                $('#audio')[0].play();

                var x = 3
                for (i of msg['choices']) {
                    $(`#choices .button:nth-child(${x})`).text(i);
                    x++;
                }
                $('#choices button').css('pointer-events', "auto").removeClass("red").removeClass("green");
                timer = 10.0;
                var timeoutID = setInterval(function () {
                    timer -= 0.01;
                    $('#countdown').text(timer.toFixed(2));
                }, 10);
                setTimeout(() => {
                    clearInterval(timeoutID);
                    $('#countdown').text(10);
                    getQuestion();
                }, 10000);
            }
        },
    });
};

function btn_clicked() {
    $('#choices button').click(function () {
        $('#choices button').css('pointer-events', "none");
        if ($(this).text() == answer) {
            $('#score').text((parseFloat($('#score').text()) + timer).toFixed(2));
            $(this).addClass("green");
            $('#added').text('+' + timer.toFixed(2))
            $('#added').transition({
                animation: 'fade',
                duration: '3s',
                onComplete: function () {
                    $('#added').text("");
                    $('#added').transition('fade');
                },
            });
        } else {
            $(this).addClass("red");
            $(this).transition('shake', '500ms');
            $(`#choices button:contains(${answer})`).addClass("green");
        }
    });
}