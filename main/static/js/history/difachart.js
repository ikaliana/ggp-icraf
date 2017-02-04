function difachart(id, xData, yData) {
    Highcharts.chart(id, {

        title: {
            text: 'Cumulative Habitat(%)'
        },

        xAxis: {
            categories: xData
        },

        yAxis: {
            title: {
                text: null
            }
        },

        tooltip: {
            crosshairs: true,
            shared: true,
            valueSuffix: ' %',
        },

        legend: {
        },

        series: [{
            name: 'Cumulative Habitat(%)',
            data: yData,

            zIndex: 1,
            marker: {
                fillColor: 'white',
                lineWidth: 2,
                lineColor: Highcharts.getOptions().colors[0]
            }
        }]
    });
}
