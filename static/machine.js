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
}

$(document).ready(function() {
    $('#users').DataTable( {
        "ajax": "/api/users/",
        "processing": true,
        "serverSide": true,
    } );
} );
