// Bind the click event for the Get Captcha button
function bindCaptchaBtnClick() {
    $("#captcha_btn").on("click",
        function (event) {
            var $this = $(this);
            var email = $("input[name='email']").val();
            if (!email) {
                alert("Please enter your email address first");
                return;
            }

            // Sending network requests through JS: Ajax
            $.ajax({
                url: "/captcha/",
                method: "POST",
                data: {
                    "email": email
                },
                success: function (res) {
                    var code = res['code'];
                    if (code === 200) {
                        $this.off("click");     //Off click event
                        // Start the countdown
                        var countDown = 60;
                        var timer = setInterval(function () {
                            countDown -- ;
                                if (countDown > 0) {
                                    $this.text("Resend in " + countDown + " seconds");
                                } else {
                                    $this.text("Get Captcha ");
                                    bindCaptchaBtnClick();      //Rebind the click event
                                    clearInterval(timer);       //Turn off timer
                                }
                            },
                            1000)
                        alert("Captcha sent successfully")
                    } else {
                        alert(res['message'])
                    }
                }

            })
        });
}



// Wait until the page documents are loaded before executing
$(function () {
    bindCaptchaBtnClick();
});