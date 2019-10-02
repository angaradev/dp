//Функция для открытия ответов на комментарии
jQuery(function($){
    var test = $('.my-btn-reply')//.parent().children('.comment-reply');

    test.click(function(event){
        event.preventDefault();
        $(this).parent().children('.comment-reply').fadeToggle();
    });



});


$(document).ready(function(){
    // Это код для правых фильтров отправка по чекбоксу
    $('input[type=checkbox]').on('change', function() {
        $(this).closest("form").submit();
    });
    // Конец кода отправки по чекбоксу

    var cart_button = $('.cart_button');
    cart_button.on('click', function(e){
    e.preventDefault();
    var pk = $(this).attr('data-pk');
    data = {
        product_id: pk
    }
    $.ajax({
        type: "GET",
        url: "/addtocart/",
        data: data,
        success: function(data){
            $('.tt-badge-cart').html(data.cartItemCount);
            }
        });
    });

    var remove_button = $('.remove-button');
    remove_button.on('click', function(e){
        e.preventDefault();
        let pk = $(this).attr('data-pk');
        data = {
            product_id: pk
        }
        $.ajax({
            type: "GET",
            url: "/removefromcart/",
            data: data,
            success: function(data){
                $('.tt-badge-cart').html(data.cartItemCount);
                $('#cart-item-' + pk).css('display', 'none');
                $('#cart-itogo').html('&#x20bd; ' + parseFloat(data.cart_total).toFixed(2));
            }
        });
    });

    let quantity_input = $('.cart-item-quantity');
    quantity_input.on('change', function(e){
        qty = $(this).val();
        item_id = $(this).attr('data-id');
        data = {
            quantity: qty,
            item_id: item_id
        }
        $.ajax({
            type: "GET",
            url: "/updatecart/",
            data: data,
            success: function(data){
                $('#price-subtotal-' + item_id).html('&#x20bd; ' + data.item_total);
                $('#cart-itogo').html('&#x20bd; ' + parseFloat(data.cart_total).toFixed(2));
            }
        });
            
    })
    //Alert before cart cleaning
    let clear_cart = $('#clear-cart');
    clear_cart.on('click', function(e){
       return confirm("Точно хотите очистить корзину?");
    });
});











