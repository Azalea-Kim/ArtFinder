//show cart action
(function () {
    const cartInfo = document.getElementById('cart-info');
    const cart = document.getElementById('cart');

    cartInfo.addEventListener('click', function () {
        cart.classList.toggle('show-cart');
    })

})();


//add item to the cart
(function () {

    const cartBtn = document.querySelectorAll('.store-item-icon');

    cartBtn.forEach(function (btn) {
        btn.addEventListener('click', function (event) {


            if (event.target.parentElement.classList.contains('store-item-icon')) {

                let fullPath = event.target.parentElement.previousElementSibling.src;
                let pos = fullPath.indexOf('img') + 3;
                let imgPath = fullPath.slice(pos);

                const item = {};
                item.img = `img-cart${imgPath}`;

                let name = event.target.parentElement.parentElement.nextElementSibling.children[0].children[0].textContent;
                item.name = name;

                $.ajax({
                    url: 'http://127.0.0.1:5000/placeOrder',
                    data: JSON.stringify({"name": name}),
                    type: 'post',
                    dataType: "json",
                    contentType: "application/json",
                    success: function (result) {
                        console.log(result);
                        alert(result['msg'])
                        // if (result['status'] === 200) {
                        //     window.location.href = "/orders"
                        // } else if (result['status'] === 400) {
                        //     window.location.href = "/cart"
                        // }

                    },
                    error: function () {
                        console.log('error')

                    }
                })


                let price = event.target.parentElement.parentElement.nextElementSibling.children[0].children[1].textContent;
                let finalPrice = price.slice(1).trim();
                item.price = finalPrice;

                //console.log(item);

                const cartItem = document.createElement('div');
                cartItem.classList.add('cart-item', 'd-flex', 'justify-content-between', 'text-capitalize', 'my-3')
                cartItem.innerHTML = `
                <img src="${item.img}" class="img-fluid rounded-circle" id="item-img" alt="">
                <div class="item-text">
                    <p id="cart-item-title" class="font-weight-bold mb-0">${item.name}</p>
                    <span>$</span>
                    <span id="cart-item-price" class="cart-item-price" class="mb-0">${item.price}</span>
                </div>
<!--                <a href="#" id='cart-item-remove' class="cart-item-confirm">confirm</a>-->
                <i class="fas fa-trash"></i>
                </a>
                </div>
                
`;


                //select cart
                const cart = document.getElementById('cart');
                const total = document.querySelector('.cart-total-container');
                cart.insertBefore(cartItem, total);
                showTotals();

            }
        });
    });

    //show cart total
    function showTotals() {
        const total = [];
        const items = document.querySelectorAll('.cart-item-price');

        items.forEach(function (item) {
            total.push(parseFloat(item.textContent));
        });

        const totalCost = total.reduce(function (total, item) {
            total += item;
            return total;
        }, 0)

        document.getElementById('cart-total').textContent = totalCost;
        document.querySelector('.item-total').textContent = totalCost;
        document.getElementById('item-count').textContent = total.length;
    }

    //submit total amount
    function submitAmount() {

    }
})();


$('#submitbtn').click(function (e) {
    e.preventDefault();
    var totalmoney = $('#cart-total').text();
    $.ajax({
        url: 'http://127.0.0.1:5000/purchase',
        data: JSON.stringify({"totalmoney": totalmoney}),
        type: 'post',
        dataType: "json",
        contentType: "application/json",
        success: function (result) {
            console.log(result);
            alert(result['msg'])
            if (result['status'] === 200) {
                window.location.href = "/orders"
            } else if (result['status'] === 400) {
                window.location.href = "/cart"
            }

        },
        error: function () {
            console.log('error')

        }
    })
})

function bindBtn2Click() {
    $("#btn2").on("click",
        function (event) {
            var $this = $(this);
            $.ajax({
                url: "http://127.0.0.1:5000/changeEmail",
                method: "POST",
                success: function (res) {
                    alert("Changed email privacy")
                }

            })
        });
}


// Wait until the page documents are loaded before executing
$(function () {
    bindBtn2Click();
});

