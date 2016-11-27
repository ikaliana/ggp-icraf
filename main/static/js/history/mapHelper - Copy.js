  //var range_color = [ "#fef0d9","#fdcc8a","#fc8d59","#e34a33","#b30000"];
  var range_color = [ "#ffffd4","#fed98e","#fe9929","#d95f0e","#993404"];
  var minval = 0;
  var maxval = range_value[range_value.length];
  var polygon_border_color = "#fbc02d";
  var polygon_blank_color = "#ccc"
  var road_color = "#999";

  function getColorIndex(value) {
    var maxlength = range_color.length;
    var tmp = value; // / 1000;

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
    var fillColor = (cIndex >= 0) ? range_color[cIndex] : polygon_blank_color;

    return { color: polygon_border_color, weight: 1, fillColor: fillColor, fillOpacity: .6 };
  }

  function getOnFeatureMouseOver(e) {
    var layer = e.target;
    info.update(layer.feature.properties);
  }

  function getOnFeatureMouveOut(e) {
    baselayer.forEach(function(layer) { layer.layer.resetStyle(e.target); });
    info.update();
  }

  function getOnEachFeature(feature,layer) {
    layer.on({
        mouseover: getOnFeatureMouseOver,
        mouseout: getOnFeatureMouveOut
    });
  }

  function numberWithCommas(x) {
    if (x<0) return "N/A";
    x = Math.round(x * 100) / 100;
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  function getInfoOnAdd(map) {
    this._div = L.DomUtil.create('div', 'card');
    this.update();
    return this._div;
  }

  function getInfoOnUpdate(props) {
    var strInfo = "";
    
    if (props) {
      strInfo = info_template.replace("[DISTRICT]", props.KABKOTA);
      strInfo = strInfo.replace("[DATA]", numberWithCommas(props.DATA));
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

    var header_legend = header_legend_template.replace("[COLOR]",road_color);
    // header_legend += "<strong>LEGEND</strong><br>";
    // header_legend += "<span class='legend-item' style='border: none'><img style='margin:0' src='" + icon_url + "'></span>District capital<br>"
    // header_legend += "<span class='legend-item' style='border: none'><hr style='height:2px;border:none;background:" + road_color + "'></span>Road<br>"
    // header_legend += legend_title;

    div_legend.innerHTML = header_legend + legend_item;

    return div_legend;
  }

  function onPointToLayer(feature,latlng) {
    var greenIcon = L.icon( {iconUrl: icon_url, iconSize: [16,16]} );
    var cm = L.marker(latlng, {icon: greenIcon})
    cm.bindTooltip(feature.properties.Kota, { permanent: true, direction: 'right' });
    return cm;
  }

  
  var map = new L.Map("map");
  var baselayers = {};
  var bounds = null;

  baselayer.forEach(function(layer) {
    var mapData = L.geoJson(layer.data, { style: getStyle, onEachFeature: getOnEachFeature });
    if (layer.baseBound) bounds = mapData.getBounds();
    if (layer.addtoMap) mapData.addTo(map);
    if (layer.addtoControl) baselayers[layer.title] = mapData;
    layer.layer = mapData;
  })

  var grp = L.layerGroup();
  $.getJSON(geojson_city_url,function(data){
    var layer = L.geoJson(data,{pointToLayer: onPointToLayer});
    grp.addLayer(layer);
  });

  var grp2 = L.layerGroup();
  $.getJSON(geojson_road_url,function(data){
    var layer = L.geoJson(data,{ weight: 1, color: road_color});
    grp2.addLayer(layer);
  });

  grp.addTo(map);
  grp2.addTo(map);

  if(bounds != null)  { map.fitBounds(bounds); /* map.setZoom(map.getZoom() + 0.5);*/ }
  if(bounds == null) baselayers = null;

  var overlayMaps = { "Road": grp2, "Cities": grp };
  var layerControls = L.control.layers( baselayers, overlayMaps, { position:"topleft", collapsed: false } ).addTo(map);

  // var info = L.control({ position: "topleft" });
  // info.onAdd = getInfoOnAdd;
  // info.update = getInfoOnUpdate;
  // info.addTo(map);

  // var legend = L.control({ position: "bottomleft" });
  // legend.onAdd = getLegendOnAdd;
  // legend.addTo(map);

  map.on('baselayerchange',function(baselayer){ 
    if(grp2._map != null) grp2.eachLayer(function (layer) { layer.bringToFront(); });
  });

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
