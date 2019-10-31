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

    //Функции для вставки в очистку ядра и разбиение на инфо и коммерческие ядра
    $('.clean-kernel').on('click', function(e){
        e.preventDefault();
        $.ajax({
            url: '/dictionary/splitkernelclean/',
            method: 'GET',
            success: function(json_data){
                $('.alert-success-my').html('<div class="alert alert-success"><strong>Успешно!</strong> ' + json_data.insert_count + ' строк Удалено из ядра!</div>');

            }
        });
    });

    $('.split-kernel').on('click', function(e){
        e.preventDefault();
        $('#loading-image').show();
        $.ajax({
            url: '/dictionary/splitkernel/',
            method: 'GET',
            success: function(json_data){
                $('.alert-success-my').html('<div class="alert alert-success"><strong>Успешно!</strong> Вставлено ' + json_data.info_count + ' строк! В Инфо запросы. И ' + json_data.comm_count + ' в Коммерческие запросы</div>');

            },
            complete: function(){
                $('#loading-image').hide();
            }
        });
    });

    //Функции для категоризатора на AJAX
    //
    
    $('#categorize-me').on('click', function(e){
        e.preventDefault();
        $('#loading-image').show();
        $.ajax({
            url: '/dictionary/categorizer/',
            method: 'GET',
            data: {'mode': 'categorize'},
            success: function(json_data){
                $('#show-counts').html('Прокатегоризировалось Ядро:<span class="bgreen"> ' + json_data.f  + '</span><span class="bgreen">Успешно: ' + json_data.i + '</span>.<span class="bred2"> Неуспешно: ' + json_data.j + '</span>');
            },
            complete: function(){
                $('#loading-image').hide();
            }
        })


    })

});
