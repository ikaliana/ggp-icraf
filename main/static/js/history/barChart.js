!function(){
  var BarChart={};
  
  function wrap(text, width, finishline) {
    text.each(function() {
      var text = d3.select(this),
          words = text.text().split(/\s+/).reverse(),
          word,
          line = [],
          lineNumber = 0,
          lineHeight = 1.1, // ems
          x = text.attr("x")
          y = text.attr("y"),
          dy = parseFloat(text.attr("dy")),
          tspan = text.text(null).append("tspan").attr("x", x).attr("y", y).attr("dy", dy + "em");
      
      while (word = words.pop()) {
        line.push(word);
        tspan.text(line.join(" "));
        if (tspan.node().getComputedTextLength() > width) {
            line.pop();
            tspan.text(line.join(" "));
            line = [word];
            tspan = text.append("tspan").attr("x", x).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
        }
      }

      if (finishline >= 0) {
        var x1 = Math.round(x) + width * 0.25, y1 = Math.round(y) + ( (lineNumber) * 16.5 ) + 5;
        d3.select(this.parentNode).append("polyline").attr("fill","none").attr("stroke","black").attr("opacity",0.5)
          .attr("points", x1 + "," + y1 + " " + x1 + "," + Math.round(finishline));
      }
    });
  }

  BarChart.vertical = function(id, data,margin_left,margin_top,number_of_ticks,bar_class,charttitle,x_lable) {

    var $container = $("#" + id), width = $container.width(), height = $container.height(); 
    if(width < 250) width = 250; if (height < 300) height = 300;

    var title_top = height - 35;
    height -= 35;
    
    margin_left = (margin_left < 1) ? width*margin_left : margin_left;
    margin_top = (margin_top < 1) ? height*margin_top : margin_top;
    if(margin_left == 0) margin_left = 25;
    margin_left += 25;
    height -= margin_top; width -= margin_left;

    var g = d3.select("#"+id).append("g").attr("transform", "translate(" + margin_left + ",0)");

    g.append("g").attr("transform", "translate(0," + title_top + ")")
      .append("text")
      .attr("x", (width/2)).attr("y",30)
      .attr("font-size","24px").attr("font-weight","500")
      .attr("text-anchor","middle").attr("alignment-baseline","baseline")
      .text(charttitle);

    var x = d3.scaleBand().rangeRound([0, width]).padding(0.1);
    x.domain(data.map(function(d) { return d.x }));

    var y = d3.scaleLinear().rangeRound([height, 0]);
    y.domain([0 , d3.max(data, function(d) { return d.y; }) ]);

    var xAxis = d3.axisBottom(x);
    var yAxis = d3.axisLeft(y).ticks(number_of_ticks).tickSize(0);

    g.append("g").attr("class","labelx").attr("transform", "translate(0," + height + ")").call(xAxis);
    ybar = g.append("g").call(yAxis);
    ybar.append("text").attr("text-anchor","middle").attr("fill","#000").attr("font-size","12").attr("transform", "rotate(-90)")
      .attr("y",-35).attr("x",-height/2).text(x_lable);

    var bar = g.selectAll(".bar")
      .data(data)
      .enter();
      
    bar.append("rect")
      .attr("class", 'tooltipped' +' ' +bar_class)      
      .attr("x", function(d) { return x(d.x); })
      .attr("y", function(d) { return y(d.y); })
      .attr("width", x.bandwidth())
      .attr("height", function(d) { return (height - y(d.y) < 0) ? 0 : height - y(d.y); })   
      .attr('data-position','top')  
      .attr('data-delay',0)   
      .attr('data-tooltip',function(d) { 
         // return charttitle + ' ' + d.x + ': '  +  + d.y + ' ' + x_lable  ;
         return d.x + ': '  +  + d.y + ' ' + x_lable  ;
      });

           
    bar.append("text")
      .attr("x", function(d) { return x(d.x) + x.bandwidth() / 2; })
      .attr("y", function(d) { return y(d.y); })
      .attr("dy", function(d) { return ((height - y(d.y)) < 25) ? -10 : 25; })
      .attr("text-anchor", "middle" )
      .attr("font-weight","bold")      
      .text(function(d) { return d.y; });
      // .text(function(d) { return /*d.y*/ d3.format(".2n")(d.y); });
      
  $('.tooltipped').tooltip();
    svg.selectAll(".labelx .tick text").call(wrap, x.bandwidth(), -1);   

  }

  BarChart.horizontal = function(id,data,margin_left,margin_top,number_of_ticks,bar_class,charttitle,x_lable) {

    var $container = $("#" + id), width = $container.width(), height = $container.height(); 
    if(width < 250) width = 250; if (height < 300) height = 300;

    var title_top = height - 35;
    height -= 35;
    
    margin_left = (margin_left < 1) ? width*margin_left : margin_left;
    margin_top = (margin_top < 1) ? height*margin_top : margin_top;
    if(margin_top == 0) margin_top = 25;
    height -= margin_top; width -= margin_left;

    var g = d3.select("#"+id).append("g").attr("transform", "translate(" + margin_left + ",0)");

    g.append("g").attr("transform", "translate(0," + title_top + ")")
      .append("text")
      .attr("x", (width/2)).attr("y",30)
      .attr("font-size","24px").attr("font-weight","500")
      .attr("text-anchor","middle").attr("alignment-baseline","baseline")
      .text(charttitle);

    var x = d3.scaleLinear().range([0, width]);
    x.domain([0 , d3.max(data, function(d) { return d.y; }) ]);

    var y = d3.scaleBand().rangeRound([0, height]).padding(0.1);
    y.domain(data.map(function(d) { return d.x }));

    var xAxis = d3.axisBottom(x).ticks(number_of_ticks).tickSize(0);
    var yAxis = d3.axisLeft(y);

    var xbar = g.append("g").attr("transform", "translate(0," + height + ")").call(xAxis);
    xbar.append("text").attr("text-anchor","middle").attr("fill","#000").attr("font-size","12")
      .attr("x",width/2).attr("y","25").text(x_lable);

    g.append("g").call(yAxis);

    var bar = g.selectAll(".bar")
      .data(data)
      .enter();

    bar.append("rect")
      .attr("class", 'tooltipped' +' ' +bar_class)     
      .attr("x", 1)
      .attr("y", function(d) { return y(d.x); })
      .attr("width", function(d) { return x(d.y); })
      .attr("height", y.bandwidth())
      .attr('data-position','top')  
      .attr('data-delay',0)        
      .attr('data-tooltip',function(d) { 
        // return charttitle + ' ' + d.x + ': '  +  + d.y + ' ' + x_lable  ;
        return d.x + ': '  +  + d.y + ' ' + x_lable  ;
      });
   
    bar.append("text")
      .attr("x", function(d) { return x(d.y); })
      .attr("y", function(d) { return y(d.x) + y.bandwidth() / 2; })
      .attr("dx", function(d) { return (x(d.y) < 50) ? 5 : -5 })
      .attr("dy", ".35em")
      .attr("text-anchor", function(d) { return (x(d.y) < 50) ? "start" : "end" })
      .attr("font-weight","bold")
      .text(function(d) { return d.y; });
      // .text(function(d) { return d3.format(".2n")(d.y); });

       $('.tooltipped').tooltip();
  
    //d3.select(id).append("div").attr("class", "card-panel card-content").append("strong").text(charttitle);

  }

  BarChart.SingleStackedHorizontal = function(id,data,margin_left,margin_top,number_of_ticks,charttitle) {
    var color = d3.scaleOrdinal(d3.schemeCategory10.slice(0).reverse());
    color.domain(d3.keys(data[0]).filter(function(key) { return key !== "label"; }));
    var divider = 1000;

    data.forEach(function(d) {
      var total = 0, y0 = 0, maxval = -1;
      d.percent_value = {};

      color.domain().forEach(function(name) { 
        if (d[name]>maxval) mxval=d[name]; 
        total += d[name];
      });

      color.domain().forEach(function(name) { 
        d.percent_value[name] = Math.round( (d[name]/total)*10000 ) / 100;
      });

      divider = (maxval > 150000) ? 1000000 : 1000;
      
      d.values = color.domain().map( function(name) { 
        var tmp = d[name];
        // var tmp2 = d[name]/divider;
        var tmp2 = Math.round( (d[name]/divider) * 100) / 100;
        return {name: name, y0: y0, y1: y0 += +d.percent_value[name], v: tmp2, v2: tmp}; 
      });
      d.total = (color.domain().length!=0) ? d.values[d.values.length - 1].y1 : 0;
    })

    var $container = $("#" + id), width = $container.width(), height = $container.height(); 
    if(width < 250) width = 250; if (height < 300) height = 300;

    var title_top = height - 35;
    height -= 35;
    
    margin_left = (margin_left < 1) ? width*margin_left : margin_left;
    margin_top = (margin_top < 1) ? height*margin_top : margin_top;
    height -= margin_top; width -= margin_left;

    var g = d3.select("#"+id).append("g").attr("transform", "translate(" + margin_left + ",0)");

    g.append("g").attr("transform", "translate(0," + title_top + ")")
      .append("text")
      .attr("x", (width/2)).attr("y",30)
      .attr("font-size","24px").attr("font-weight","500")
      .attr("text-anchor","middle").attr("alignment-baseline","baseline")
      .text(charttitle);

    var y = d3.scaleBand().rangeRound([0, height]).padding(0.1);
    y.domain(data.map(function(d) { return d.label; }));
    var yAxis = d3.axisLeft(y);
    var linestop = y.bandwidth();

    var x = d3.scaleLinear().range([0, width]);
    x.domain([0, d3.max(data, function(d) { return d.total; })+5]);
    var xAxis = d3.axisBottom(x).ticks(number_of_ticks).tickSize(0) //.tickFormat(d3.format(".2s"));
      .tickFormat(function(d){ return d + "%"; })
      // .tickFormat(function(d){ return d3.format(".2s")(d) + "%"; })
    g.append("g").attr("transform", "translate(0," + height + ")").call(xAxis)

    var bar = g.selectAll(".label").data(data).enter()
      .append("g").attr("transform", function(d) { return "translate(0," + y(d.label) + ")"; });

    var bar_enter = bar.selectAll("rect").data(function(d) { return d.values; }).enter();

    bar_enter.append("rect")
      .attr("x", function(d) { return x(d.y0); })
      .attr("y", y.bandwidth()*0.7)
      .attr("width", function(d) { return x(d.y1) - x(d.y0); })
      .attr("height", y.bandwidth()*0.3)
      .style("fill", function(d) { return color(d.name); });

    var text_width = width / data[0].values.length;

    bar_enter.append("polyline")
      .attr("fill","none").attr("stroke","black").attr("opacity",0.5)
      .attr("points", function(d,i) {
        var x1 = text_width * i + text_width * 0.25;
        var y1 = linestop*0.6;
        var x2 = x(d.y0) + (x(d.y1) - x(d.y0)) / 2;
        var y2 = y.bandwidth() * 0.7 + 5;
        return x1 + "," + y1 + " " + x2 + "," + y2; 
      });

    bar_enter.append("text")
      .attr("class","label-text")
      .text(function(d) { return d.name + ", " + d3.format(".2n")(d.v); })
      .attr("x", function(d,i,a) { return text_width*i; })
      .attr("y", function(d,i) { return ((i % 2) ? 0.2 : 0.4)*y.bandwidth(); })
      .attr("dy", 0);

    svg.selectAll(".label-text").call(wrap, text_width, linestop*0.6);

    //d3.select(id).append("div").attr("class", "card-panel card-content").append("strong").text(charttitle);
  }

  BarChart.StackedVertical = function(id,data,margin_left,margin_top,number_of_ticks,charttitle,color_scheme,x_lable) {
    var $container = $("#" + id), width = $container.width(), height = $container.height(); 
    if(width < 250) width = 250; if (height < 300) height = 300;

    var title_top = height - 35;
    height -= 35;
    
    margin_left = (margin_left < 1) ? width*margin_left : margin_left;
    margin_top = (margin_top < 1) ? height*margin_top : margin_top;
    if(margin_left == 0) margin_left = 25;
    margin_left += 25;
    height -= margin_top; width -= margin_left;

    var x = d3.scaleBand().rangeRound([0, width]).padding(0.1);
    var y = d3.scaleLinear().rangeRound([height, 0]);
    var z = d3.scaleOrdinal().range(color_scheme);
    var stack = d3.stack();

    x.domain(xkeys);
    var xAxis = d3.axisBottom(x);
    y.domain([0, d3.max(data, function(d) { return d.total; })]).nice();
    z.domain(zkeys);

    var g = d3.select("#"+id).append("g").attr("transform", "translate(" + margin_left + ",0)");

    g.append("g").attr("transform", "translate(0," + title_top + ")")
      .append("text")
      .attr("x", (width/2)).attr("y",30)
      .attr("font-size","24px").attr("font-weight","500")
      .attr("text-anchor","middle").attr("alignment-baseline","baseline")
      .text(charttitle);

    g.append("g").attr("class","labelx").attr("transform", "translate(0," + height + ")").call(xAxis);

    g.selectAll(".serie")
      .data(stack.keys(zkeys)(data))
      .enter().append("g")
        .attr("class", "serie")
        .attr("fill", function(d) { return z(d.key); })
      .selectAll("rect")
      .data(function(d) { return d; })
      .enter().append("rect")
        .attr("x", function(d) { return x(d.data.period); })
        .attr("y", function(d) { return y(d[1]); })
        .attr("height", function(d) { return y(d[0]) - y(d[1]); })
        .attr("width", x.bandwidth());

    g.selectAll(".text-series")
      .data(stack.keys(zkeys)(data)).enter().append("g")
        .attr("class", "serie-label")
      .selectAll("text")
      .data(function(d) { return d; })
      .enter().append("text")
        .attr("text-anchor","middle")
        .attr("alignment-baseline",function(d) {
          var h = y(d[0]) - y(d[1]);
          return (h<15) ? "baseline" : "middle"; 
        })
        .attr("x", function(d) { return x(d.data.period) + x.bandwidth()/2; })
        .attr("y", function(d) {
          var h = y(d[0]) - y(d[1]);
          return (h<15) ? y(d[0]) : y(d[0])-h/2; 
        })
        .text(function(d) { return Math.round( (d[1]-d[0]) * 100 )/100; });
        
    g.append("text").attr("text-anchor","middle").attr("fill","#000").attr("font-size","16").attr("transform", "rotate(-90)")
      .attr("y",-10).attr("x",-height/2).text(x_lable);
  }
  
  this.BarChart = BarChart;
}();