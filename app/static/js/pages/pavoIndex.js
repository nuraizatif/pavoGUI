$(function () {
    //Widgets count
    $('.count-to').countTo();

    //Sales count to
    $('.sales-count-to').countTo({
        formatter: function (value, options) {
            return '$' + value.toFixed(2).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, ' ').replace('.', ',');
        }
    });

    new Chart(document.getElementById("pie_chart").getContext("2d"), getChartJs('pie'));
    initSparkline();
});

function initSparkline() {
    $(".sparkline").each(function () {
        var $this = $(this);
        $this.sparkline('html', $this.data());
    });
}

var data = [], totalPoints = 110;
function getRandomData() {
    if (data.length > 0) data = data.slice(1);

    while (data.length < totalPoints) {
        var prev = data.length > 0 ? data[data.length - 1] : 50, y = prev + Math.random() * 10 - 5;
        if (y < 0) { y = 0; } else if (y > 100) { y = 100; }

        data.push(y);
    }

    var res = [];
    for (var i = 0; i < data.length; ++i) {
        res.push([i, data[i]]);
    }

    return res;
}

function getChartJs(type) {
    var config = null;
    
    if (type === 'pie') {
        config = {
            type: 'pie',
            data: {
                datasets: [{
                    data: [225, 150, 40],
                    backgroundColor: [
                        "rgb(139, 195, 74)",
                        "rgb(255, 193, 7)",
                        "rgb(233, 30, 99)"
                    ],
                }],
                labels: [
                    "Accepted",
                    "No Run",
                    "Failed"
                ]
            },
            options: {
                responsive: true,
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        fontColor: 'rgb(0, 0, 0)'
                    }
                }
            }
        }
    }
    return config;
}