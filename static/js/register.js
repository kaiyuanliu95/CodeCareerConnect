$(document).ready(function() {
    $('#registrationForm').submit(function(event) {
        event.preventDefault(); // Prevent form default submission behavior

        var registrationData = {
            email: $('#email').val(),
            password: $('#password').val(),
            username: $('#username').val()
        };

        $.ajax({
            type: 'POST',
            url: '/register',
            contentType: 'application/json',
            data: JSON.stringify(registrationData),
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    window.location.href = '/'; // Redirect to home page on successful registration.
                } else {
                    alert(response.message); // Show an alert if registration fails.
                }
            },
            error: function() {
                alert('Registration failed. Please check your network connection.');
            }
        });
    });
});