$(document).ready(function(){
    $('textarea').on('keypress', function(e) {
        if (e.which == 13){
            var formdata = $('form').serialize();
            
            $.ajax({
                url: '/dictionary/kernelclean/',
                type: 'POST',
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

                }
            });

        }                    
    });
   //For loading negative words to form clean kernel and working on info queries 
    var elem = $('#myid');
    var elem2 = $('#myid2');
    load_kernel(elem, 'clean');
    load_kernel(elem2, 'info');
    function load_kernel(elem, mode){
    elem.on('click',function(e){
        e.preventDefault();
        $.ajax({
            url: '/dictionary/loadkernel/',
            type: 'GET',
            data: {'kernel_mode': mode},
            success: function(json_data){
                $('textarea').val(json_data.minus);
                console.log(json_data.minus);
                }
            })
        })
    }
});
