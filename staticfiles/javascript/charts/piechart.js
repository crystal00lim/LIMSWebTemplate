document.addEventListener('DOMContentLoaded', function() {
    const series = JSON.parse(document.getElementById('pie_series').textContent);
    const labels = JSON.parse(document.getElementById('pie_labels').textContent);

    var pieChart = new ApexCharts(
        document.querySelector("#pieChart"), {
            chart: {width: 500, type: 'pie'},
            title: {text: 'WGS Species', align: 'center'},
            series: series,
            labels: labels,
            responsive: [{
                breakpoint: 480,
                options: {
                    chart: {width: 200}, 
                    legend: {position: 'bottom'}
                }
            }]
        }
    );
    pieChart.render();
})