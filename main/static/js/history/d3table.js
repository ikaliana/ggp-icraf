function GenerateTableD3(container,tabledata,header,columnheadermap,tableclass,headerclass, id) {
    var table_class = (tableclass == "") ? "compact" : tableclass;
    var header_class = (headerclass == "") ? "grey lighten-1" : headerclass;

    var table = d3.select(container).append("table").attr("class",table_class).attr('id', (id == undefined ? '' : id));



    table.append('thead').append('tr').attr("class",header_class).selectAll('th')
        .data(header).enter()
        .append('th').text(function (column) { return column; });

    var tbody = table.append('tbody');

    var rows = tbody.selectAll('tr').data(tabledata).enter().append('tr');
   
    var cells = rows.selectAll('td')
        .data(function (row) {
            return new_data = columnheadermap.map(function (column) { return {column: column, value: row[column]}; });
        })
        .enter().append('td')
            .text(function (d) { return d.value; });	
    

    
}
function GenerateTableD3DataTable(container,tabledata,header,columnheadermap,tableclass,headerclass, id, options, fixedCol = false) {
    var table_class = (tableclass == "") ? "compact" : tableclass;
    var header_class = (headerclass == "") ? "grey lighten-1" : headerclass;

    var table = d3.select(container).append("table").attr("id",id). attr("class",table_class)

    table.append('thead').append('tr').attr("class",header_class).selectAll('th')
        .data(header).enter()
        .append('th').text(function (column) { return column; });

    var tbody = table.append('tbody');

    var rows = tbody.selectAll('tr')
    
    .data(tabledata).enter().append('tr');
  
    var cells = rows.selectAll('td')
        .data(function (row) {
            return new_data = columnheadermap.map(function (column) { return {column: column, value: row[column]}; });
        })
        .enter().append('td')
            .html(function (d) { return d.value; });	
    
    
    // un-remark datatables 
    var oTable = $('#' + id).DataTable(options);

    // $('select').material_select();
    $('select').addClass('browser-default')
    
}

function GenerateTableD3TableLock(container,tabledata,header,columnheadermap,tableclass,headerclass, id, options) {
    var table_class = (tableclass == "") ? "compact" : tableclass;
    var header_class = (headerclass == "") ? "grey lighten-1" : headerclass;

    var table = d3.select(container).append("table").attr("id",id). attr("class",table_class)

    table.append('thead').append('tr').attr("class",header_class).selectAll('th')
        .data(header).enter()
        .append('th').text(function (column) { return column; })
        .attr('class',function(d, i) { return (i == 0) ? "locked" :   "";  });

    var tbody = table.append('tbody');

    var rows = tbody.selectAll('tr')
    
    .data(tabledata).enter().append('tr');
  
    var cells = rows.selectAll('td')
        .data(function (row) {
            return new_data = columnheadermap.map(function (column) { return {column: column, value: row[column]}; });
        })
        .enter().append('td')
            .html(function (d) { return d.value; })
            .attr('class', function(d,i) { return (i == 0) ? "row_locked" :   "";  });	
    
    
    // un-remark datatables 
    TableLock(id,null,null,"locked");
    
}