$(document).ready(function() {
        //function my_func(){
        var elem = $('#f-canv');
        var endpoint = '/api/chart/data/';
        var labels = [];
        var defaultData = [];
        $.ajax({
            method: "GET",
            url: endpoint,
            success: function(data){
                labels = data.labels;
                defaultData = data.defaultData;
                bgColors = data.bgColors;
                borderColor = data.borderColor;
                var ctx = document.getElementById('f-canv').getContext('2d');
                var myChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: '# Работа с ФОТО',
                            data: defaultData,
                            backgroundColor: bgColors,
                            borderColor: borderColor,
                            borderWidth: 1
                        }]
                    },
//                    options: {
//                        scales: {
//                            yAxes: [{
//                                ticks: {
//                                    beginAtZero: true
//                                }
//                            }]
//                        }
//                    }
                });
            }
        });



});
