!function(){
  var BarChart={};
  
  BarChart.horizontal = function(id, data,margin_left,margin_top,number_of_ticks,bar_class,charttitle) {

    var $container = $("#" + id), width = $container.width(), height = $container.height(); 
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

    var bar = g.selectAll(".bar")
      .data(data)
      .enter();
    bar.append("rect")
      .attr("class", bar_class)
      .attr("x", function(d) { return x(d.x); })
      .attr("y", function(d) { return y(d.y); })
      .attr("width", x.bandwidth())
      .attr("height", function(d) { return height - y(d.y); });
    bar.append("text")
      .attr("x", function(d) { return x(d.x) + x.bandwidth() / 2; })
      .attr("y", function(d) { return y(d.y); })
      .attr("dy", function(d) { return ((height - y(d.y)) < 25) ? -10 : 25; })
      .attr("text-anchor", "middle" )
      .attr("font-weight","bold")
      .text(function(d) { return d3.format(".2n")(d.y); });

    d3.select(id).append("div").attr("class", "card-panel card-content").append("strong").text(charttitle);
  }

  BarChart.vertical = function(id,data,margin_left,margin_top,number_of_ticks,bar_class,charttitle) {

    var $container = $("#" + id), width = $container.width(), height = $container.height(); 
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

    var bar = g.selectAll(".bar")
      .data(data)
      .enter();
    bar.append("rect")
      .attr("class", bar_class)
      .attr("x", 1)
      .attr("y", function(d) { return y(d.x); })
      .attr("width", function(d) { var w = width - y(d.x); if(w<0) w=1; return w; })
      .attr("height", y.bandwidth()); //;
    bar.append("text")
      .attr("x", function(d) { var w = width - y(d.x); if(w<0) w=1; return w; })
      .attr("y", function(d) { return y(d.x) + y.bandwidth() / 2; })
      .attr("dx", function(d) { return ((width - y(d.x)) < 50) ? 5 : -5 })
      .attr("dy", ".35em")
      .attr("text-anchor", function(d) { return ((width - y(d.x)) < 50) ? "start" : "end" })
      .attr("font-weight","bold")
      .text(function(d) { return d3.format(".2n")(d.y); });

    d3.select(id).append("div").attr("class", "card-panel card-content").append("strong").text(charttitle);

  }
  
  this.BarChart = BarChart;
}();