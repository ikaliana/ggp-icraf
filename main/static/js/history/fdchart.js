function GenerateSvg(targetChart) {
    var tmp = d3.select(targetChart).append("svg").attr("width", '100%').attr("height", "400").attr("id",targetChart);
    var $container = $(targetChart).parent(), width = $container.width(), height = $container.height();
    if (width < min_width) width = min_width;
    if (height < min_width) height = min_height;
    tmp.attr('viewBox','0 0 '+ width +' '+ height ).attr('preserveAspectRatio','xMinYMin');

    var defs = tmp.append("g").attr("class", "defs").append("defs");
    defs.append("marker")
        .attr("id", "end-arrow") 
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", "10")
        .attr("markerWidth", 7)
        .attr("markerHeight", 7)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5")
        .attr("fill", "#000");
    var filter = defs.append("filter").attr("id","txt-background")
        .attr("x",0).attr("y",0)
        .attr("width",1).attr("height",1);
        //<feFlood flood-color="yellow"/>
    filter.append("feFlood").attr("flood-color","#fff");
        //<feComposite in="SourceGraphic"/>
    filter.append("feComposite").attr("in","SourceGraphic");

    return tmp;
}

function RepairData(d) {
    return { 
        id: d.Nodes,
        Nodes: d.Nodes, 
        Size: +d.Size,
        InDegree: +d.InDegree,
        OutDegree: +d.OutDegree,
        //Eigenvalue: +d.Eigenvalue,
        Eigenvalue: Math.round(+d.Eigenvalue * 1000) / 1000,
        Group: d.Group,
        Type: d.Type,
        GroupType: d.GroupType  
    }
}

function RepairDataLink(d) {
    return {
        source: d.source,
        target: d.target,
        width: +d.width
    }
}

function LoadNodes(target, path, filename, data) {
    //console.log(language)
    d3.csv(path + filename + "_links_" + language + ".csv"
        ,RepairDataLink
        ,function(d) { LoadLinks(target,path,filename,data,d); });
}

function LoadLinks(target, path,filename,node_data,link_data) {
    var svg = GenerateSvg(target);
    var width = $("#" + target).width(), height = $("#" + target).height();

    delete node_data["columns"];
    delete link_data["columns"];
    //console.log(link_data)

    var groups = [];
    var groups_detail = {};

    node_data.forEach(function (d,i) {
        var radius = Math.round(d.Size/4);
        d.radius = (radius<2) ? 2 : radius;
        d.arrowIndex = i;
        groups.push(d.Group);
        if(!groups_detail.hasOwnProperty(d.Group)) 
            groups_detail[d.Group] = {id: d.Group, type: d.Type, group: d.GroupType};
        //d.fx = Math.round(Math.random() * (width - radius * 2) + radius);
        //d.fy = Math.round(Math.random() * (height - radius * 2) + radius);
    });

    groups = groups.filter((x, i, a) => a.indexOf(x) == i);  //distinct group
    //console.log(groups,groups_detail);
    var max_radius = Math.round( d3.max(node_data, function(d) { return d.radius; }) ) + 1;
    var graph = {"nodes": node_data, "links": link_data};

    var link = svg.append("g").attr("class", "links").selectAll(".line")
        .data(graph.links)
        //.enter().append("line")
        .enter().append("path")
        .style("fill","none").attr("stroke","#999")
        .style("marker-end", "url(#end-arrow)");

    var node = svg.append("g").attr("class", "nodes").selectAll(".circle")
        .data(graph.nodes).enter()
        .append("circle")
        .attr("id", function(d) { return "node" + d.arrowIndex; })
        .call(d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended))
        .attr("fill", function(d) { return color(groups.indexOf(d.Group)); })
        .style("stroke", function(d) { return d3.rgb(color(groups.indexOf(d.Group))).darker(); })
        .append("title").text(function(d) { return d.id; });;

    var text = svg.append("g").attr("class", "labels").selectAll(".text")
        .data(graph.nodes).enter()
        .append("text").text(function(d) { return d.id; })
        //.attr("filter","url(#txt-background)")
        .attr("fill", function(d) { return color(groups.indexOf(d.Group)); })
        .attr("text-anchor", "middle")
        .attr("font-weight", 500)
        .attr("font-size", 12);

    var flink = d3.forceLink();
    flink.id(function(d) { return d.id; });
    flink.distance(max_radius);

    var fc = d3.forceCollide();
    fc.radius(function(d) { return max_radius + 0.5; });
    fc.iterations(2);

    var simulation = d3.forceSimulation();
    simulation.force("link", flink);
    simulation.force("charge", d3.forceManyBody().strength(-100));
    simulation.force("center", d3.forceCenter(width / 2, height / 2));
    simulation.force("collide", fc);

    simulation.nodes(graph.nodes).on("tick", ticked);
    simulation.force("link").links(graph.links);

    function ticked() {
        //node
        d3.selectAll("circle")
            .attr("r", function(d) { return d.radius; })
            .attr("cx", function(d) { return d.x = Math.max(d.radius+3, Math.min(width - d.radius - 10, d.x)); })
            .attr("cy", function(d) { return d.y = Math.max(d.radius+3, Math.min(height - d.radius - 10, d.y)); });
            // .attr("cx", function(d) { return d.x; })
            // .attr("cy", function(d) { return d.y; });

        d3.selectAll("text")
            .attr("x", function (d) { return d.x; })
            .attr("y", function (d) { return d.y; })
            .attr("dy", function(d) { return d.radius + 15; });

        link
            .attr("d", function(d) {
                var dx = d.target.x - d.source.x, dy = d.target.y - d.source.y,
                    dr = Math.sqrt(dx * dx + dy * dy);

                var a = Math.atan(dy/dx);
                var mx = (dx != 0) ? dx/Math.abs(dx) : 0, my = (dy != 0) ? dy/Math.abs(dy) : 0;

                var x1 = d.source.x + d.source.radius * Math.cos(Math.abs(a)) * mx;
                var y1 = d.source.y + d.source.radius * Math.sin(Math.abs(a)) * my;
                var x2 = d.target.x + d.target.radius * Math.cos(Math.abs(a)) * -mx;
                var y2 = d.target.y + d.target.radius * Math.sin(Math.abs(a)) * -my;

                if(d.target != d.source) 
                    return "M" + x1 + "," + y1 + "A" + dr + "," + dr + " 0 0,1 " + x2 + "," + y2;
                else {
                    //console.log(d.source.radius,dy,dx,a)
                    x1 = d.source.x + d.source.radius + 5;
                    y1 = d.source.y; //+ d.source.radius;
                    return "M" + x1 + "," + y1 + "A20,20 0 1,1 " + (x1+1) + "," + (y1+1);
                }

                //return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
                //return "M" + x1 + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
            });
        
        // link
        //     .style("marker-end", function(d) { return "url(#node" + d.target.arrowIndex + ")"; })
        //     .attr("x1", function(d) { return d.source.x; })
        //     .attr("y1", function(d) { return d.source.y; })
        //     .attr("x2", function(d) { return d.target.x; })
        //     .attr("y2", function(d) { return d.target.y; });
    }

    /* GENERATE TABLE FOR NODES */
    var columns = ["Type","Group","Factor","InDegree","OutDegree","Eigenvalue"];
    var columns_key = ["Type","GroupType","Nodes","InDegree","OutDegree","Eigenvalue"];
    
    //class="responsive-table"
    var table = d3.select(target + "table").append("table").attr("class","compact responsive-table")

    table.append('thead').append('tr').attr("class","grey lighten-1").selectAll('th')
        .data(columns).enter()
        .append('th').text(function (column) { return column; });

    var tbody = table.append('tbody');

    var rows = tbody.selectAll('tr').data(node_data).enter()
        .append('tr')
        .style("background", function(d) { return color(groups.indexOf(d.Group)); });
        //.style("background", function(d) { return d3.rgb(color(groups.indexOf(d.Group))).brighter(); });

    var cells = rows.selectAll('td')
        .data(function (row) {
            var group = row.Group;
            return new_data = columns_key.map(function (column) {
                return {column: column, value: row[column], group: group};
            });
        })
        .enter().append('td')
            .style("color", function(d) { return d3.rgb(color(groups.indexOf(d.group))).brighter(1.5); })
            .text(function (d) { return d.value; });

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
}

// function dragstarted(d) {
//     if (!d3.event.active) simulation.alphaTarget(0.3).restart();
//     d.fx = d.x;
//     d.fy = d.y;
// }

// function dragged(d) {
//     d.fx = d3.event.x;
//     d.fy = d3.event.y;
// }

// function dragended(d) {
//     if (!d3.event.active) simulation.alphaTarget(0);
//     d.fx = null;
//     d.fy = null;
// }

