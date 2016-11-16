!function(){
  var BarChart={};
  
  BarChart.horizontal = function(id, data,margin_left,margin_top,number_of_ticks,bar_class) {

    var $container = $("#" + targetChart), width = $container.width(), height = $container.height(); 
    margin_left = (margin_left < 1) ? width*margin_left : margin_left;
    margin_top = (margin_top < 1) ? height*margin_top : margin_top;
    var g = d3.select("#"+id).append("g").attr("transform", "translate(" + margin_left + ",0)");
    height -= margin_top; width -= margin_left;

    var x = d3.scaleBand().rangeRound([0, width]).padding(0.1);
    x.domain(data.map(function(d) { return d.x }));

    var y = d3.scaleLinear().rangeRound([height, 0]);
    y.domain([0 , d3.max(data, function(d) { return d.y; }) ]);

    var xAxis = d3.axisBottom(x);
    var yAxis = d3.axisLeft(y).ticks(number_of_ticks).tickSize(0);

    g.append("g").attr("transform", "translate(0," + height + ")").call(xAxis);
    g.append("g").call(yAxis);

    g.selectAll(".bar")
      .data(data)
      .enter().append("rect")
      .attr("class", bar_class)
      .attr("x", function(d) { return x(d.x); })
      .attr("y", function(d) { return y(d.y); })
      .attr("width", x.bandwidth())
      .attr("height", function(d) { return height - y(d.y); });

  }

  BarChart.vertical = function(id,data,margin_left,margin_top,number_of_ticks,bar_class) {

    var $container = $("#" + targetChart), width = $container.width(), height = $container.height(); 
    margin_left = (margin_left < 1) ? width*margin_left : margin_left;
    margin_top = (margin_top < 1) ? height*margin_top : margin_top;
    var g = d3.select("#"+id).append("g").attr("transform", "translate(" + margin_left + ",0)");
    height -= margin_top; width -= margin_left;

    var x = d3.scaleLinear().range([0, width]);
    x.domain([0 , d3.max(data, function(d) { return d.y; }) ]);

    var y = d3.scaleBand().rangeRound([0, height]).padding(0.1);
    y.domain(data.map(function(d) { return d.x }));

    var xAxis = d3.axisBottom(x).ticks(number_of_ticks).tickSize(0);
    var yAxis = d3.axisLeft(y);

    g.append("g").attr("transform", "translate(0," + height + ")").call(xAxis);
    g.append("g").call(yAxis);

    g.selectAll(".bar")
      .data(data)
      .enter().append("rect")
      .attr("class", bar_class)
      .attr("x", 1)
      .attr("y", function(d) { return y(d.x); })
      .attr("width", function(d) { return width - y(d.x); })
      .attr("height", y.bandwidth());
  }
  
  this.BarChart = BarChart;
}();