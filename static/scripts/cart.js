$(document).ready(function () {
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
        })
    }
    function RefreshTotal(Input) {
        let total = 0;
        if (Input == null) {
            $('.item').each(function () {
                const prodcutPrice = parseFloat($(this).children('.price').children('.price_text').text());
                const productQty = parseFloat($(this).children('quantity').children('book_amount').text());
                total += prodcutPrice;
            })
            $('#total_price').text(total);
        }
        else{
            const unitPriceInput = $(Input).parent().parent().children('.Author').children('.original_price');
            const priceInput = $(Input).parent().parent().children('.price').children('.price_text');;
            const qty = parseFloat($(Input).parent().children('.book_amount').text());
            priceInput.text(parseFloat(unitPriceInput.text()) * qty);
        }
    }
    function blink(Input, txt){
        $(Input).FadeOut(200, function(){
            Input.text(txt);
            Input.FadeIn(200)
        })
    }
});