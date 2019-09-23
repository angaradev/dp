//Функция для открытия ответов на комментарии
jQuery(function($){
    var test = $('.my-btn-reply')//.parent().children('.comment-reply');

    test.click(function(event){
        event.preventDefault();
        $(this).parent().children('.comment-reply').fadeToggle();
    });


});