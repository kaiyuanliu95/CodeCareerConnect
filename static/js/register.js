function bindEmailCaptchaClick() {
  $("#captcha-btn").click(function (event) {
      // this: jQuery object means the current button
      var $this = $(this);
      // Block default events
      event.preventDefault();

      var email = $("input[name='email']").val();
      console.log("Email captured:", email); 
      $.ajax({
          url: "/auth/captcha/email",
          method: "POST",
          data: JSON.stringify({ email: email }),
          contentType: "application/json",
          success: function (result) {
              var code = result['code'];
              if (code == 200) {
                  var countdown = 60;
                  // Before starting the countdown, cancel the click event of the button
                  $this.off("click");
                  var timer = setInterval(function () {
                      $this.text(countdown);
                      countdown -= 1;
                      // Executed at the end of the countdown
                      if (countdown <= 0) {
                          // clear timer
                          clearInterval(timer);
                          // Button text restored
                          $this.text("Get Varification Code.");
                          // Rebind click event
                          bindEmailCaptchaClick();
                      }
                  }, 1000);
                  $("#success-message").text("Email Varification Code Send Success!").show();
                  setTimeout(function () {
                      $("#success-message").hide(); // Hide message after 3 seconds
                  }, 3000);
              } else {
                  alert(result['message']);
              }
          },
          error: function (error) {
              console.log(error);
          }
      });
  });
}

// Execute after the entire web page is loaded
$(function () {
  bindEmailCaptchaClick();
});
