// using jQuery
//These functions are to make sure Django plays nicely via POST for CSRF requests
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

function message(msg, colour) {
    if (!colour) {
        colour = "red";
    }

    $("#message").html("<p style='color:" + colour + "'>" + msg + "</p>");
    $("#message").slideDown("fast");
    setTimeout(function() { $("#message").slideUp("fast"); }, 5000);
}

function sortPress(a,b) {
    if (a.time < b.time) {
        return -1;
    } else if (b.time > a.time) {
        return 1;
    }
    return 0;
}

function performAnalysis() {
    var sortedPresses = keyPresses.sort(sortPress);
    var keyStrokes = JSON.stringify(sortedPresses)
    var username = $("#username").val();
    var password = $("#password").val();

    $.ajax({
        type: "POST",
        url: "/api/saveAnalysis",
        data: {"username": username, "password": password, "keyStrokes": keyStrokes},
        dataType: "json"
    }).done(function(data) {
        if (data.result === 1) {
            message("Successfully saved login attempt", "black");
        } else {
            message("An unknown error occurred. If this continues, please submit a bug ticket to: github.com/sjrumsby/machine-learning-passwords");
        }

        clearLogin();
    }).fail(function() {
        message("An unknown error occurred. If this continues, please submit a bug ticket to github.com/sjrumsby/machine-learning-passwords");
    });
}

function logKeyPress(e) {
    if (e.type == "keypress") {
        console.log(e);
    }

    if (e.type == "keyup") {
        if (e.which == 8 || e.which == 46) {
            message("Woah now - we can't handle making mistakes. Try again");
            clearLogin();
            return 0;
        }

        if ($.inArray(e.which, [35,36,37,38,39,40]) != -1) {
            message("Stop trying to confuse me with your fancy navigation! Again!");
            clearLogin();
            return 0;
        }
    }

    var pressTime = window.performance.now();
    var element = document.activeElement.id;

    var keyCode = e.keyCode;

    if (keyCode === 0) {
        keyCode = e.charCode;
    }

    console.log(keyCode)

    var press = {
        "action": e.type,
        "time": pressTime,
        "key": e.key,
        "element": element,
        "keyCode": keyCode,
    };

    keyPresses.push(press)
}

function clearLogin() {
    $("#username").val("");
    $("#password").val("");
    keyPresses = []
}


function testLogin() {
    var username = $("#username").val();
    var password = $("#password").val();

    if (!username || !password) {
        console.log("Username or password were submitted null");
        return;
    }

    $.ajax({
        type: "POST",
        url: "/api/login",
        data: {"username": username, "password": password},
        dataType: "json"
    }).done(function(data) {
        if (data.result === 1) {
            performAnalysis();
        } else {
            message("Login failed. Not performing machine learning analysis");
        }

        clearLogin();
    }).fail(function() {
        message("An unknown error occurred. If this continues, please submit a bug ticket to github.com/sjrumsby/machine-learning-passwords");
    });
}

function create_user() {
    var sername = $("#username").val();
    var password = $("#password").val();

    if (password.length < 8) {
        message("Password length must be at least 8 characters for training purposes");
        return;
    }

    $.ajax({
        type: "POST",
        url: "/api/users/create",
        data: {"username": username, "password": password},
        dataType: "json"
    }).done(function(data) {
        if (data.result === 1) {
            message("Succesfully created a new user. Now train the algorithm!", "black");
        } else {
            if (data.error_msg) {
                message(data.error_msg);
            } else {
                message("An unknown error occurred. If this continues, please submit a bug ticket to github.com/sjrumsby/machine-learning-passwords");
            }
        }
    }).fail(function() {
        message("An unknown error occurred. If this continues, please submit a bug ticket to github.com/sjrumsby/machine-learning-passwords");
    });
}

function trainUserButton() {
    var user_id = $('#trainSelect').val();

    if (user_id) {
        var current_url = window.location.href;
        new_url = current_url + "/" + user_id
        window.location = new_url
    } else {
        message("Invalid user_id. If this continues, please submit a bug ticket to github.com/sjrumsby/machine-learning-passwords");
    }
}

$(document).ready(function() {
    keyPresses = [];
    $("#username").val("")
    $("#password").val("")
    $('#users').DataTable( {
        "ajax": "/api/users/",
        "processing": true,
        "serverSide": true,
    });
    $("#train_user_button").on("click", function() { trainUserButton(); });

    $(".machineLearn").on("keydown", function(e) { logKeyPress(e); });
    $(".machineLearn").on("keyup", function(e) { logKeyPress(e); });
    $(".machineLearn").on("keypress", function(e) { logKeyPress(e); });
});

