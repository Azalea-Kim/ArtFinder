
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

//   遮罩蒙版
var dropdown = document.getElementsByClassName("splicing")[0];
var dropdownLiItem = dropdown.getElementsByClassName("splicing-item-img");
console.log(dropdown);
console.log(dropdownLiItem);
for (var i = 0; i < 4; i++) {
    dropdownLiItem[i].onmouseover = function () {
        var dropdownLi = this.getElementsByTagName("div")[0];
        dropdownLi.classList.remove("img-title")
    }
    dropdownLiItem[i].onmouseout = function () {
        var dropdownLi = this.getElementsByTagName("div")[0];
        dropdownLi.classList.add("img-title");
    }
}