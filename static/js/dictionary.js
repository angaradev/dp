$(document).ready(function(){
    $('textarea').on('keypress', function(e) {
        if (e.which == 13){
            var formdata = $('form').serialize();
            
            $.ajax({
                url: '/dictionary/mainwork/',
                type: 'GET',
                data: formdata,
                success: function(json_data){
                    var obj = JSON.parse(json_data.keys);
                    var ul = '<ul>';
                    if (!$.isEmptyObject(obj)){
                        $.each(obj, function(key, value){
                        ul += ('<li>' + value.fields.keywords + '<span class="float-right bgreen">' + value.fields.freq + '</spna></li>');
                        });
                    ul = ul + '</ul>'
                    var kernel = $('#kernel_id');
                    kernel.html(ul)
                    }else{
                        var kernel = $('#kernel_id');
                        kernel.html('Ничего не найдено или уже обработано');
                    }
                    var obj2 = JSON.parse(json_data.noms);
                    var ul2 = '<ul>';
                    if (!$.isEmptyObject(obj2)){
                        $.each(obj2, function(key2, value2){
                            ul2 += '<li>' + value2.fields.name + '</li>';
                        });
                        ul2 = ul2 + '</ul>';
                        var noms = $('#noms_id').html(ul2);
                    }else{
                        var noms = $('#noms_id');
                        noms.html('Ничего не найдено или уже обработано');
                    }

                }
            });

        }                    
    });
    
    $('#id_group_name').blur(function(){
        var group_data = $(this).val()
        $.ajax({
            url: '/dictionary/checkgroup/',
            type: 'GET',
            data: {'group_data': group_data},
            success: function(chk_group){
                if (group_data == chk_group.group_name){
                    alert('Такая группа есть');
                    $('#id_plus').val(chk_group.plus);
                    $('#id_minus').val(chk_group.minus);
                    $('#id_parent').val(chk_group.parent_cat);
                }
            }
        }); 
    });

    var chk_gr = $('.chk-gr');
    $('.chk-gr').on('click', function(e){
        e.preventDefault();
        var group_data = $(this).attr('data-pk');
        $.ajax({
            url: '/dictionary/checkgroup/',
            type: 'GET',
            data: {'group_data': group_data},
            success: function(chk_group){
                if (group_data == chk_group.group_name){
                    alert('Такая группа есть');
                    $('#id_plus').val(chk_group.plus);
                    $('#id_minus').val(chk_group.minus);
                    $('#id_parent').val(chk_group.parent_cat);
                    $('#id_group_name').val(chk_group.group_name);
                }
            }
        }); 

    });

});
