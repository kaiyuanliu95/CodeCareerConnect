$(document).ready(function() {
    $('#loginForm').submit(function(event) {
        event.preventDefault(); // Prevent form default submission behavior

        var loginData = {
            email: $('#email').val(),
            password: $('#password').val()
        };

        $.ajax({
            type: 'POST',
            url: '/login',
            contentType: 'application/json',
            data: JSON.stringify(loginData),
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    window.location.href = '/home';  // Redirect to home page on success.
                } else {
                    alert(response.message);  // Show an alert if login fails.
                }
            },
            error: function() {
                alert('Login failed. Please check your network connection.');
            }
        });
    });
});


