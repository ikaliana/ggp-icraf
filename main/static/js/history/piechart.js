(function( $ ){
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

	var methods = {
		el: "",
		init : function(options) {
			var clone = jQuery.extend(true, {}, options["data"]);
			
			methods.el = this;			
			methods.setup(clone, options["width"], options["height"], options["r"], options["ir"], options["color"], options["title"]);
		},
		getArc: function(radius, innerradius){
			var arc = d3.arc()
				.innerRadius(innerradius)
				.outerRadius(radius);
				
			return arc;
		},
		setup: function(dataset, w, h, r, ir, c, title){
			
			var padding = 0;
		
			this.width = w;
			this.height = h;
			this.radius = r
			this.innerradius = ir;
			
			this.color = c; //d3.schemeCategory20;
			
			this.pie = d3.pie()
				.sort(null)
				.value(function(d) { return d.total; });
				
			this.arc = this.getArc(this.radius, this.innerradius);
			
			// this.svg = d3.select(methods.el["selector"]).append("svg")
			// 	.attr("width", this.width + padding)
			// 	.attr("height", this.height + padding)
			// 	.append("g")
			// 		.attr("class", "piechart")
			// 		.attr("transform", "translate(" + ((this.width/2) + (padding/2)) + "," + ((this.height/2) + (padding/2)) + ")");				
			this.svg = d3.select(methods.el["selector"])
				.append("g")
				.attr("class", "piechart")
				.attr("transform", "translate(" + ((this.width/2) + (padding/2)) + "," + ((this.height/2) + (padding/2)-25) + ")");		

			d3.select(methods.el["selector"]).append("g").attr("class","piechart_title")
				.attr("transform", "translate(0," + (this.height - 35) + ")")	
				.append("text")
				.attr("x", this.width/2).attr("y",30)
				.attr("font-size","24px").attr("font-weight","500")
				.attr("text-anchor","middle").attr("alignment-baseline","baseline")
				.text(title);		

            this.segments = this.svg.append("g")
					.attr("class", "segments");
            
            this.labels = this.svg.append("g")
					.attr("class", "labels");

            this.pointers = this.svg.append("g")
					.attr("class", "pointers");
            
            
		},
		oldPieData: "",
		pieTween: function(r, ir, d, i){
			var that = this;
			
			var theOldDataInPie = methods.oldPieData;
			// Interpolate the arcs in data space

			var s0;
			var e0;

			if(theOldDataInPie[i]){
					s0 = theOldDataInPie[i].startAngle;
					e0 = theOldDataInPie[i].endAngle;
			} else if (!(theOldDataInPie[i]) && theOldDataInPie[i-1]) {
					s0 = theOldDataInPie[i-1].endAngle;
					e0 = theOldDataInPie[i-1].endAngle;
			} else if(!(theOldDataInPie[i-1]) && theOldDataInPie.length > 0){
					s0 = theOldDataInPie[theOldDataInPie.length-1].endAngle;
					e0 = theOldDataInPie[theOldDataInPie.length-1].endAngle;
			} else {
					s0 = 0;
					e0 = 0;
			}

			var i = d3.interpolate({startAngle: s0, endAngle: e0}, {startAngle: d.startAngle, endAngle: d.endAngle});
			
			return function(t) {
					var b = i(t);
					return methods.getArc(r, ir)(b);
			};
		},
		removePieTween: function(r, ir, d, i) {				
			var that = this;
			s0 = 2 * Math.PI;
			e0 = 2 * Math.PI;
			var i = d3.interpolate({startAngle: d.startAngle, endAngle: d.endAngle}, {startAngle: s0, endAngle: e0});

			return function(t) {
					var b = i(t);
					return methods.getArc(r, ir)(b);
			};
		},
		update: function(dataSet){
			var that = this;

			methods.el = this;
			var r = methods.radius; //$(methods.el["selector"]).data("r");
			var ir = methods.innerradius; //$(methods.el["selector"]).data("ir");
			
			methods.svg = d3.select(methods.el["selector"] + " .piechart");
            methods.segments = d3.select(methods.el["selector"] + " .segments");
            methods.labels = d3.select(methods.el["selector"] + " .labels");
            methods.pointers = d3.select(methods.el["selector"] + " .pointers");
			
			dataSet.forEach(function(d) {
				d.total = +d.value;
			});
			
			this.piedata = methods.pie(dataSet);
			
			//__slices
			this.path = methods.segments.selectAll("path.pie")
				.data(this.piedata);

			this.path.enter().append("path")
				.attr("class", "pie")
				.attr("fill", function(d, i) {
					return methods.color[i]; 
				})
				.transition()
					.duration(300)
					.attrTween("d", function(d, i) {
						return methods.pieTween(r, ir, d, i); 
					});
			
			this.path
					.transition()
					.duration(300)
					.attrTween("d", function(d, i) {
						return methods.pieTween(r, ir, d, i); 
					});
			
			this.path.exit()
					.transition()
					.duration(300)
					.attrTween("d", function(d, i) {
						return methods.removePieTween(r, ir, d, i); 
					})
					.remove();    
			//__slices
			
			
			//__labels	
			var labels = methods.labels.selectAll("text")
				.data(this.piedata);
				
			labels.enter()
				.append("text")
				.attr("dy",".35em")
				.attr("text-anchor", function(d) {
					d.midleAngle = d.startAngle + (d.endAngle - d.startAngle)/2;
					d.a = d.midleAngle - Math.PI/2;
					d.cosA = Math.cos(d.a);
					d.sinA = Math.sin(d.a);
					return (Math.PI < d.midleAngle) ? "begin" : "end"; //"end" : "begin";
				})
				.attr("x", function(d) {
					d.cx = d.cosA * r * 0.7; //(r-20); //(ir+((r-ir)/2));
					d.ox = d.cosA * r * 1.1;
					return (Math.PI < d.midleAngle) ? -methods.width/2 : methods.width/2;
				})
				.attr("y", function(d) {
					d.cy = d.sinA * r * 0.7; //(r-20); //(ir+((r-ir)/2));
					var a = (d.sinA > 0) ? 10 : 0;
					return d.y = d.sinA * (r + 20) + a;
				})
				.text(function(d) {
					var p = (d.endAngle - d.startAngle) / (2 * Math.PI) * 100;
					p = Math.round(p * 100)/100;
					return d.data.label + ", " + p + "%"; 
				})

			labels.exit().remove();

			methods.labels.selectAll(".labels text").call(wrap, 90, -1)
				.each(function(d) { 
					var b = this.getBBox();
					d.sx = (b.x >= 0) ? b.x-5 : b.x + b.width+5;
					d.sy = b.y + 10; //b.height/2;
				});

			var pointers = methods.pointers.selectAll("path.pointer")
				.data(this.piedata);
				
			pointers.enter()
				.append("path")
				.attr("class", "pointer")
				.style("fill", "none")
				.style("stroke", "black")
				.style("stroke-opacity",0.4)
				.attr("d", function(d) {
					return "M" + d.cx + "," + d.cy + "L" + d.ox + "," + d.sy + " " + d.sx + "," + d.sy;
				})

			pointers.exit().remove();
				
			this.oldPieData = this.piedata;
			
		}
	};

	$.fn.piechart = function(methodOrOptions) {
		if ( methods[methodOrOptions] ) {
			return methods[ methodOrOptions ].apply( this, Array.prototype.slice.call( arguments, 1 ));
		} else if ( typeof methodOrOptions === 'object' || ! methodOrOptions ) {
			// Default to "init"
			return methods.init.apply( this, arguments );
		} else {
			$.error( 'Method ' +  methodOrOptions + ' does not exist' );
		}    
	};

})(jQuery);