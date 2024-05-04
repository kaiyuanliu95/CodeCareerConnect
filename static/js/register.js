$(document).ready(function() {
    $('#registrationForm').submit(function(event) {
        event.preventDefault(); // Prevent default form submission behavior
        
        // Get form data
        var formData = {
            username: $('#username').val(),
            email: $('#email').val(),
            password: $('#password').val()
        };
        
        // Send AJAX request to the server
        $.ajax({
            type: 'POST',
            url: '/register',
            data: JSON.stringify(formData),
            contentType: 'application/json',
            success: function(response) {
                alert(response.message); // Display message returned by the server
                $('#registrationForm')[0].reset(); // Reset the form
            },
            error: function(xhr) {
                alert(xhr.responseJSON.message); // Display error message
            }
        });
    });
});
