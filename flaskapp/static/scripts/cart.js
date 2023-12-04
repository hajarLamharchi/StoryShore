$(document).ready(function () {
    var cartId;
    init();
    RefreshTotal(null);
    $('.sus_button').click(function (event) {
        let amount = 0;
        const mountInput = $(this).parent().children('.book_amount')
        const currentamount = mountInput.text();
        amount = parseInt(currentamount);
        amount = amount - 1;
        if (amount == 0) {
            removeItem(this);
        }
        else{
            update(cartId, amount)
        }
        mountInput.text(amount);
        RefreshTotal(this);
        RefreshTotal(null);
    });
    $('.add_button').click(function (event) {
        let amount = 0;
        const mountInput = $(this).parent().children('.book_amount')
        const currentamount = mountInput.text();
        amount = parseInt(currentamount);
        amount = amount + 1;
        amount = Math.min(amount, 10)
        update(cartId, amount)
        mountInput.text(amount);
        RefreshTotal(this);
        RefreshTotal(null);
    });
    $('.remove_button').click(function () {
        removeItem(this);

    });

    function removeItem(Input) {
        const productRow = $(Input).parent().parent();
        productRow.slideUp(300, function () {
            productRow.remove();
            RefreshTotal(null); 
            fetch("/removeFromCart/"+cartId,{ method: 'POST'})
            .then(Response=>{
            })
        })
    }
    function RefreshTotal(Input) {
        let total = 0;
        if (Input == null) {
            $('.item').each(function () {
                const prodcutPrice = parseFloat($(this).children('.price').children('.price_text').text());
                total += prodcutPrice;

            })
            $('#total_price').text(total.toFixed(2));

        }
        else{
            const unitPriceInput = $(Input).parent().parent().children('.Author').children('.original_price');
            const priceInput = $(Input).parent().parent().children('.price').children('.price_text');;
            const qty = parseFloat($(Input).parent().children('.book_amount').text());
            priceInput.text(parseFloat(unitPriceInput.text()) * qty);

        }
    }
    function init(){
        $('.price_text').each(function () {
            const unitPriceInput = $(this).parent().parent().children('.Author').children('.original_price');
            const qty = parseFloat($(this).parent().parent().children('.quantity').children('.book_amount').text());
            $(this).text(parseFloat(unitPriceInput.text()) * qty);

        })
    }
    window.getId = function(cartID)
    {
        cartId= cartID;
        
    }
    window.Purchase = function(){
        $("#loadingScreen").css("display", "flex");
        $(".item").each(function () {
            const Price = parseFloat($(this).children('.price').children('.price_text').text());
            const input = this
            const bookid = this.getAttribute('data-cart-id') 
            const bookId = this.getAttribute('data-book-id')

            fetch("/Purchase/"+bookId+"/"+Price ,{ method: 'POST'})
            .then(()=>{
                const productRow = $(input);
                productRow.slideUp(300, function () {
                    productRow.remove();
                    RefreshTotal(null); 
                    fetch("/removeFromCart/"+ bookid,{ method: 'POST'})
                    .then(Response=>{
                        if ($(".item").length == 0)
                        {
                            $("#loadingScreen").css("display", "none");
                        }
                    })
                })
            })
        })

    }
});

function update(cartID, qty){
    fetch("/updateCart/"+cartID+"/"+qty,{ method: 'POST'})
        .then(Response=>{
        })
}