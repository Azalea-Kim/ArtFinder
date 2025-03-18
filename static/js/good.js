
var items = document.getElementsByClassName("item");
var circles = document.getElementsByClassName("circle");
var leftBtn = document.getElementById("btn-left");
var rightBtn = document.getElementById("btn-right");
var content = document.querySelector('.content');
var index = 0;
var timer = null;
// 初始化
items[index].className = "item active";
circles[index].className = "circle white";
for (let i = 0; i < items.length; i++) {
    circles[i].setAttribute("num", i);
}

//清除class
var clearclass = function () {
    for (let i = 0; i < items.length; i++) {
        items[i].className = "item";
        circles[i].className = "circle";
        circles[i].setAttribute("num", i);
    }
}
/*只显示一个class*/
function move() {
    clearclass();
    items[index].className = "item active";
    circles[index].className = "circle white";
}
//点击右边按钮切换下一张图片
rightBtn.onclick = function () {
    if (index < items.length - 1) {
        index++;
    }
    else {
        index = 0;
    }
    move();
}
//点击左边按钮切换上一张图片
leftBtn.onclick = function () {
    if (index <= 0) {
        index = items.length - 1;
    }
    else {
        index--;
    }
    move();
}
//开始定时器，点击右边按钮，实现轮播
timer = setInterval(function () {
    rightBtn.onclick();
}, 1500)
//点击圆点时，跳转到对应图片
for (var i = 0; i < circles.length; i++) {
    circles[i].addEventListener("click", function () {
        var point_index = this.getAttribute("num");
        index = point_index;
        move();
    })
}
//鼠标移入清除定时器，并开启一个三秒的定时器，使慢慢转动
content.onmouseover = function () {
    clearInterval(timer);
    timer = setInterval(function () {
        rightBtn.onclick();
    }, 4000)
}
//鼠标移出又开启定时器
content.onmouseleave = function () {
    clearInterval(timer);
    timer = setInterval(function () {
        rightBtn.onclick();
    }, 4000)
}

////一个简单的ajax
//        function loadBasicDoc() {
//            var xhr = new XMLHttpRequest();
//            xhr.onreadystatechange=function () {
//                if(xhr.readyState == 4 && xhr.status == 200) {
//
//                    //通过Ajax响应的东西异步的展示在id为hello的div中
//                    document.getElementById("detail-content").innerHTML=xhr.responseText;
//                }
//            };
//            xhr.open("POST","basicMessage.html",true);
//            xhr.send();
//        }
//
//        function loadAdvancedDoc() {
//            var xhr = new XMLHttpRequest();
//            xhr.onreadystatechange=function () {
//                if(xhr.readyState == 4 && xhr.status == 200) {
//
//                    //通过Ajax响应的东西异步的展示在id为hello的div中
//                    document.getElementById("detail-content").innerHTML=xhr.responseText;
//                }
//            };
//            xhr.open("POST","advancedMessage.html",true);
//            xhr.send();
//        }
//
//            function loadMasterDoc() {
//            var xhr = new XMLHttpRequest();
//            xhr.onreadystatechange=function () {
//                if(xhr.readyState == 4 && xhr.status == 200) {
//
//                    //通过Ajax响应的东西异步的展示在id为hello的div中
//                    document.getElementById("detail-content").innerHTML=xhr.responseText;
//                }
//            };
//            xhr.open("POST","masterMessage.html",true);
//            xhr.send();
//        }

function confirmID(){
    console.log('in');
    var gigId = $('#gig-id').text();
    console.log(gigId);
    $.ajax({
        url: 'http://127.0.0.1:5000/placeOrder',
        data:JSON.stringify( {"gigId": gigId}),
        type: 'post',
        dataType:"json",
        contentType: "application/json",
        success: function(result){
            console.log(result)
            alert(result['msg'])


        },
        error: function(){
            console.log('error')
        }
    })

}
