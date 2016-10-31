    var x = d3.scaleBand().rangeRound([0, width]).padding(0.1);
  x.domain(barData.map(function(d) { return d.x }))

  var y = d3.scaleLinear().rangeRound([height, 0]);
  y.domain([0 , d3.max(barData, function(d) { return d.y; }) ])

  var xAxis = d3.axisBottom(x); //.ticks(10);
  var yAxis = d3.axisLeft(y).ticks(10).tickSize(0); //.tickFormat(function(d) { return d/1000; }); //.ticks(5);

  svg.append("g")
    .attr("class", "axis axis--x")
    .attr("transform", "translate(0," + height + ")")
    .text("Label")
    .call(xAxis);

  svg.append("g")
    .attr("class", "axis axis--y")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    //.style("text-anchor", "end")
    //.text("Value");

  svg.selectAll(".bar")
    .data(barData)
    .enter().append("rect")
    .attr("class", "bar")
    .attr("x", function(d) { return x(d.x); })
    .attr("y", function(d) { return y(d.y); })
    .attr("width", x.bandwidth())
    .attr("height", function(d) { return height - y(d.y); });
