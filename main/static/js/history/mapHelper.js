  function getColorIndex(value) {
    var maxlength = range_color.length;
    var range = (maxval - minval) / maxlength;
    if (value > maxval || value < minval) return -1;

    for ( i = 0; i < maxlength; i++ ) {
      if( (value-minval) >= range*i && (value-minval) < range*(i+1) ) { return i; }
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
    mapData.resetStyle(e.target);
    info.update();
  }

  function getOnEachFeature(feature,layer) {
    // var strpop = "";
    // strpop += "<strong>" + feature.properties.KABKOTA + "</strong>";
    // strpop += "<br>Area: " + feature.properties.DATA;
    // layer.bindPopup( strpop );
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
    var range = (maxval - minval) / maxlength;

    var legend_item = "";
    for ( i = 0; i < maxlength; i++ ) {
      
      legend_item += "<span class='legend-item' style='background: " + range_color[i] + "'></span> ";
      legend_item += numberWithCommas(Math.round(range*i + minval)) + " &ndash; ";
      legend_item += numberWithCommas(Math.round(range*(i+1)) + minval);
      //if( (value-minval) >= range*i && (value-minval) < range*(i+1) ) { return i; }
      legend_item += "<br>";
    }

    div_legend.innerHTML = legend_item;

    return div_legend;
  }

  var map = new L.Map("map");
  var range_color = [ "#fef0d9","#fdcc8a","#fc8d59","#e34a33","#b30000"];

  var mapData = L.geoJson(geojson_data, { style: getStyle, onEachFeature: getOnEachFeature });
  mapData.addTo(map);
  map.fitBounds(mapData.getBounds());

  var info = L.control();
  info.onAdd = getInfoOnAdd;
  info.update = getInfoOnUpdate;
  info.addTo(map);

  var legend = L.control({ position: "bottomleft" });
  legend.onAdd = getLegendOnAdd;
  legend.addTo(map);