function GenerateTableD3(container,tabledata,header,columnheadermap,tableclass,headerclass) {
    var table_class = (tableclass == "") ? "compact" : tableclass;
    var header_class = (headerclass == "") ? "grey lighten-1" : headerclass;

    var table = d3.select(container).append("table").attr("class",table_class)

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
function GenerateTableD3DataTable(container,tabledata,header,columnheadermap,tableclass,headerclass, id) {
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
    
    /*
    un-remark datatables 
    $('#' + id).DataTable({});
    $('select').material_select();
    */
}