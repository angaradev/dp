$(document).ready(function(){
    $('.chk-div').on('click', function(){
        var pk = $(this).attr('data-id');
        var inp = $(this).next(':input');
        inp.attr('checked', true);
        $(this).addClass('img-bord');
    });  
});
