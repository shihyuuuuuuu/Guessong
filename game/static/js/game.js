$(document).ready(function () {
    $('#final_score').hide();
    $('#start_btn').click(function () {
        if ($('#nickname').val() != "") {
            $('#choices button').css('pointer-events', "none");
            $('#score').text(0);
            $("#choices .button").text('???');
            getQuestion($('#nickname').val());
            $('#start_area').hide();
            $('#choices').show();
            $('#final_score').hide();
            $('.link').hide();
            $('#nickname').css("border", "1px solid rgba(34,36,38,.15)");
        } else {
            $('#nickname').css("border", "1px solid red");
        }
    });
    $('#final_score button').click(function () {
        window.location.href = "leaderboard/";
    });
    answer = "";
    btnClicked();
});

function getQuestion(nickname) {
    $.get({
        url: '',
        data: {
            'start': true,
            'nickname': nickname,
        },
        success: function (msg) {
            if (msg['endGame']) {
                $('#choices').hide();
                $('#final_score').show();
                $('#final_score span').text($('#score').text());
                updateLeaderBoard();
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
                var timeIntervalID = setInterval(function () {
                    timer -= 0.01;
                    $('#countdown').text(timer.toFixed(2));
                }, 10);
                setTimeout(() => {
                    clearInterval(timeIntervalID);
                    $('#countdown').text(10);
                    getQuestion();
                }, 10000);
            }
        },
    });
};

function btnClicked() {
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

function updateLeaderBoard() {
    $.post({
        url: 'updateleader/',
        data: {
            'nickname': $('#nickname').val(),
            'score': parseFloat($('#score').text()),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function () { },
    });
}