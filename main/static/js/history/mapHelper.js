  var range_color = [ "#fef0d9","#fdcc8a","#fc8d59","#e34a33","#b30000"];
  var range_value = [50,100,250,350,500];
  var minval = 0;
  var maxval = range_value[range_value.length];
  var geojsonMarkerOptions = {
    radius: 5,
    fillColor: "#ff7800",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
  };


  function getColorIndex(value) {
    var maxlength = range_color.length;
    var tmp = value / 1000;

    if (tmp > maxval || tmp < minval) return -1;
    if (tmp < range_value[0] ) return 0

    for ( i = 1; i < maxlength; i++ ) {
      if( tmp >= range_value[i-1] && tmp < range_value[i] ) { return i; }
    }

    return maxlength-1;
  }

  function getStyle(feature) {
    var luas = feature.properties.DATA;
    var cIndex = getColorIndex(luas);
    var fillColor = (cIndex >= 0) ? range_color[cIndex] : "#ccc";

    return { color: "#999", weight: 1, fillColor: fillColor, fillOpacity: .6 };
  }

  function getOnFeatureMouseOver(e) {
    var layer = e.target;
    info.update(layer.feature.properties);
  }

  function getOnFeatureMouveOut(e) {
    mapData1.resetStyle(e.target);
    mapData2.resetStyle(e.target);
    info.update();
  }

  function getOnEachFeature(feature,layer) {
    layer.on({
        mouseover: getOnFeatureMouseOver,
        mouseout: getOnFeatureMouveOut
    });
  }

  function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  function getInfoOnAdd(map) {
    this._div = L.DomUtil.create('div', 'card');
    this.update();
    return this._div;
  }

  function getInfoOnUpdate(props) {
    var strInfo = "";
    
    if (props && commodity_title != "&nbsp;") {
      strInfo += commodity_title + " in <strong>" + props.KABKOTA + "</strong>";
      strInfo += "<br>Area: <strong>" + numberWithCommas(props.DATA) + "</strong>";
    }

    var div = L.DomUtil.create("div", "card-content");
    div.innerHTML = strInfo;

    this._div.innerHTML = (props) ? div.outerHTML : strInfo;
  };

  function getLegendOnAdd(map) {
    var div_legend = L.DomUtil.create("div", "card-panel card-content");
    var maxlength = range_color.length;

    var legend_item = "";
    for ( i = 0; i < maxlength; i++ ) {
      
      var lval = (i==0) ? 0 : range_value[i-1];
      var rval = range_value[i];

      legend_item += "<span class='legend-item' style='background: " + range_color[i] + "'></span> ";
      legend_item += lval + " &ndash; ";
      legend_item += rval;
      legend_item += "<br>";
    }
    var header_legend = "<h6>" + commodity_title + " area<br><span style='font-size:smaller'>(thousand hectare)</span></h6>";
    div_legend.innerHTML = header_legend + legend_item;

    return div_legend;
  }

  function onPointToLayer(feature,latlng) {
    var cm = L.circleMarker(latlng, geojsonMarkerOptions);
    cm.bindTooltip(feature.properties.Kota, { permanent: true, direction: 'right' });
    return cm;
  }

  var map = new L.Map("map");

  var mapData1 = L.geoJson(geojson_data1, { style: getStyle, onEachFeature: getOnEachFeature });
  var mapData2 = L.geoJson(geojson_data2, { style: getStyle, onEachFeature: getOnEachFeature });
  mapData2.addTo(map);

  var grp = L.layerGroup();
  $.getJSON(geojson_city_url,function(data){
    var layer = L.geoJson(data,{pointToLayer: onPointToLayer});
    grp.addLayer(layer);
  });

  var grp2 = L.layerGroup();
  $.getJSON(geojson_road_url,function(data){
    var layer = L.geoJson(data,{ weight: 1, color: "#8bc34a" });
    grp2.addLayer(layer);
  });

  grp.addTo(map);
  grp2.addTo(map);

  map.fitBounds(mapData2.getBounds());

  var baselayers = {};
  baselayers[period_value[0]] = mapData1;
  baselayers[period_value[1]] = mapData2;  

  var overlayMaps = { "Road": grp2, "Cities": grp };

  L.control.layers( baselayers, overlayMaps, { collapsed: false } ).addTo(map);

  var info = L.control();
  info.onAdd = getInfoOnAdd;
  info.update = getInfoOnUpdate;
  info.addTo(map);

  var legend = L.control({ position: "bottomleft" });
  legend.onAdd = getLegendOnAdd;
  legend.addTo(map);

//leaflet control hack!!!
  var classname = "leaflet-control-layers-selector";
  var label_classname = classname + "-label"
  
  $( "." + classname ).each(function(idx) {
    var type = $(this).attr("type");
    var input_id = ((type=="radio") ? $(this).attr("name")  : "layer-control-checkbox") + "-" + idx;

    var span = $(this).next();
    var item_text = span.text();

    var new_item = "<label class='" + label_classname + "' for='" + input_id + "''>" + item_text + "</label>"

    var new_class = (type=="radio") ? "with-gap" : "filled-in";

    $(this).addClass(new_class);
    $(this).attr("id",input_id)
    span.remove();
    $(this).after(new_item);
  });
