$(document).ready(function(){
    //add all event handlers here
    console.log("Adding event handlers");
    $("#account").on("change", check_username);
    console.log("functions registered");
});

function check_username(){
    //get the source elemrnt
    console.log("check_username called");
//    var chosen_user = $(this).find("input");
    var chosen_user = document.getElementById("account").value
    $("#checkuser").removeClass();
    $("#checkuser").html('<img src="static/images/loading.gif" class="loadinggif" height="20px" width="20px">');
    console.log(chosen_user);

    //ajax code
    $.post('/checkuser', {
        'username': chosen_user//field value being sent to the server
    }).done(function (response){
        var server_response = response['text']
        var server_code = response['returnvalue']
        if(server_code == 0){//success: Username does not exist in the db
            $("#password").focus();
            $("#checkuser").html('<span>'+server_response+'</span>');
            $("#checkuser").addClass("success");
        }else{//dailure:Username already exists in the db
            $("#password").focus();
            $("#checkuser").html('<span>'+server_response+'</span>');
            $("#checkuser").addClass("failure");
        }
    }).fail(function(){
        $("#checkuser").html('<span>Error contacting server</span>');
        $("#checkuser").addClass("failure");

    });
}