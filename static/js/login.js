$(document).ready(function() {
    $('#loginForm').submit(function(event) {
        event.preventDefault(); // Prevent form default submission behavior

        var loginData = {
            email: $('#email').val(),
            password: $('#password').val()// Add CSRF token
        };

        console.log("Login data: ", loginData);  // Add this line for debugging

        $.ajax({
            type: 'POST',
            url: '/login',
            contentType: 'application/x-www-form-urlencoded', // Changed content type
            data: $.param(loginData),  // Serialize the data
            success: function(response) {
                console.log("Server response: ", response);  // Add this line for debugging
                if (response.success) {
                    window.location.href = '/';  // Redirect to home page on success.
                } else {
                    if (response.errors) {
                        // Display validation errors
                        var errors = response.errors;
                        for (var field in errors) {
                            alert(errors[field]);
                        }
                    } else {
                        alert(response.message);  // Show an alert if login fails.
                    }
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error("Login request failed: ", textStatus, errorThrown);  // Add this line for debugging
                alert('Login failed. Please check your network connection.');
            }
        });
    });
});
