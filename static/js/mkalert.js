$(document).ready(function(){

    $('.mk-alert').on('click', function(){
        confirm('Вставка файла в базу займет долгое время. Уверены?');
    })

    $('.mk-alert-del').on('click', function(){
        confirm('Удалить файл? Операция необратима!');
    })

    $('.download-file').on('click', function(){
        setInterval(update, 5000);
    });
    function update(){
        location.reload();
    }
});
