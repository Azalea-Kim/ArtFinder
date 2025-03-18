function showGigs(){
    console.log('in');
    var authorId = $('#author_id').text();
    console.log('authorId '+authorId);
    $.ajax({
        url: 'http://127.0.0.1:5000/show_gigs',
        data:JSON.stringify( {"authorId": authorId}),
        type: 'post',
        dataType:"json",
        contentType: "application/json",
        success: function(result){
            console.log(result);
            gigList = result['gigList']
            console.log('gigList '+gigList);

            for(i=0; i<gigList.length; i++){
                gigdic = gigList[i];
                gig_pic = gigdic['gig_pic'];
                gig_title = gigdic['gig_title'];
                gig_author_id = gigdic['gig_author_id'];
                author_name = gigdic["gig_author_name"];
                gig_price = gigdic["gig_price"];
                gig_content = gigdic['gig_content'];
                gig_id =  gigdic['gig_id'];

                a = "http://127.0.0.1:5000/module_page/"+gig_id

                console.log("gig_pic is " + gig_pic);
                console.log("gig_title is " + gig_title);
                console.log("gig_author_id is " + gig_author_id);
                console.log("gig_content is " + gig_content);
                console.log("gig_id is " + gig_id);
                $("#display-orders").html('<div class="display-item" id="display-item" >'+
                '<div class="display-item-img"><img src="../static/pic/'+gig_pic+'" alt=""></div>'+
                '<div class="display-item-detial"><div class="detial-title">'+gig_title+'</div>'+
                '<img src = "../static/avatar/default_avatar.png" width="40px" height="40px" />'+
                '<div class="seller-name"><a href="" target="_self" class="text-semi-bold"title=""rel="nofollow noopener noreferrer">'+author_name+'</a></div>'+
                '<div class="detial-content"><a href="" target="_blank" title="I will create detailed artwork for your tshirt or merch" rel="">'+ gig_content+'</a></div>'+
                '<div class="detial-price">$ '+gig_price+'</div><div class="detial-point">');
                }
            alert(result['msg'])
        },
        error: function(){
            console.log('error')
        }
    })
}

var btn = document.getElementById('open_btn');
var div = document.getElementById('background');
var close = document.getElementById('close-button');

//btn.onclick = function show() {
//console.log("hihihi");
//	div.style.display = "block";
//}

function show() {
	div.style.display = "block";
}

function close() {
console.log("hihihi");
	div.style.display = "none";
}
//
//window.onclick = function close(e) {
//	if (e.target == div) {
//		div.style.display = "none";
//	}
//}
