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

function message(msg) {
    $("#message").html("<p>" + msg + "</p>");
    $("#message").show("fast")
    setTimeout(function() { $("#message").slideUp("fast"); }, 5000)
}


function create_user() {
    username = $("#username").val();
    password = $("#password").val();

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
            message("Succesfully created a new user. Now train the algorithm!")
        } else {
            if (data.error_msg) {
                message(data.error_msg)
            } else {
                message("An unknown error occurred. If this continues, please submit a bug ticket to github.com/sjrumsby/machine-learning-passwords")
            }
        }
    });
}

$(document).ready(function() {
    $('#users').DataTable( {
        "ajax": "/api/users/",
        "processing": true,
        "serverSide": true,
    } );
} );
