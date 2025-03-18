function setCookie(name, value, hours, path) {
  var name = escape(name);
  var value = escape(value);
  var expires = new Date();
  expires.setTime(expires.getTime() + hours * 3600000);
  path = path == "" ? "" : ";path=" + path;
  _expires = (typeof hours) == "string" ? "" : ";expires=" + expires.toUTCString();
  document.cookie = name + "=" + value + _expires + path;
}

// function passwordCheck(){
//  var account = document.getElementById("email").value;
//  var password = document.getElementById("password").value;
//  if(account!= "none" & password!= "none"){
//  if(subm()){
//    window.location.href = '../templates/home.html';
//    }else{
//      alert("The verification code is incorrect");
//    }
//  }else{
//  alert("The account or password is incorrect");
//  }

// }



function subm(){
  var val = document.getElementById("text").value;
  var num = show_num.join("");
  //document.getElementById('canvas').innerText(num);
  if(val === ''){
      alert('Please enter the verification code');
      var data ={
        'num':0
      };
      $.ajax({
          url:'/test',
          type:'POST',
          data: JSON.stringify(data),
      })
  }else if(val === num){
      var data ={
        'num':1
      };
      $.ajax({
              url:'/test',
              type:'POST',
              data: JSON.stringify(data),
              contentType : "application/json; charset=UTF-8",
          })
  }else{
      alert('Verification code error');
      var data = {
        'num':0
      };
      $.ajax({
          url:'/test',
          type:'POST',
          data: JSON.stringify(data),
          contentType : "application/json; charset=UTF-8",
      })
//      var data = {"num":0};
//      $.ajax({
//          url:'/login',
//          type:'POST',
//          data: JSON.stringify(data),
//      })
      document.getElementById("text").value='';
      draw(show_num);

  }

}