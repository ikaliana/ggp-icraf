  //var range_color = [ "#fef0d9","#fdcc8a","#fc8d59","#e34a33","#b30000"];
  var range_color = [ "#ffffd4","#fed98e","#fe9929","#d95f0e","#993404"];
  var minval = 0;
  var maxval = range_value[range_value.length];
  var polygon_border_color = "#fbc02d";
  var polygon_blank_color = "#ccc"

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
    // console.log(map_options.custom_field_name == undefined);
    var luas = (typeof map_options.custom_field_name == "undefined") ? feature.properties.DATA : feature.properties[map_options.custom_field_name];
    var cIndex = getColorIndex(luas);
    var fillColor = (cIndex >= 0) ? range_color[cIndex] : polygon_blank_color;

    return { color: polygon_border_color, weight: 1, fillColor: fillColor, fillOpacity: .6 };
  }

  function numberWithCommas(x,dec) {
    if (x<0) return "N/A";
    var num = Math.pow(10,decimal_digit);

    x = Math.round(x * num) / num;
    vals = x.toString().split(".");
    
    return vals[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",") + "." + vals[1];
    //return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  function getOnFeatureMouseOver(e) {
    var layer = e.target;
    info.update(layer.feature.properties);

    var oe = e.containerPoint; 
    var height = $(".feature-info").height();
    var left = oe.x;
    var top = oe.y;
    if (600-height < top) top -= height;
    $(".feature-info").css({top: top + 'px', left: left + 'px', position:'absolute'});
    //console.log($(".feature-info").height())
  }

  function getOnFeatureMouveOut(e) {
    baselayer.forEach(function(layer) { if(layer.type == "geojson") layer.layer.resetStyle(e.target); });
    info.update();
  }

  function getOnEachFeature(feature,layer) {
    layer.on({
        mouseover: getOnFeatureMouseOver,
        mouseout: getOnFeatureMouveOut
    });
  }

  function getInfoOnAdd(map) {
    this._div = L.DomUtil.create('div', 'card feature-info');
    this.update();
    return this._div;
  }

  function getInfoOnUpdate(props) {
    var strInfo = "";
    
    if (props) {
      var data = props.DATA;
      var disdata = (data < 0) ? "n/a" : numberWithCommas(data);
      strInfo = L.Util.template(info_template, { DISTRICT: props.KABKOTA, DATA: disdata });
      strInfo = strInfo.replace(" ","&nbsp;");
      strInfo = strInfo.replace(" ","&nbsp;");
      strInfo = strInfo.replace(" ","&nbsp;");
    }

    var div = L.DomUtil.create("div", "card-content");
    div.innerHTML = strInfo;

    this._div.innerHTML = (props) ? div.outerHTML : strInfo;
  };

  function onPointToLayer(feature,latlng) {
    var greenIcon = L.icon( {iconUrl: icon_url, iconSize: [16,16]} );
    var cm = L.marker(latlng, {icon: greenIcon})
    cm.bindTooltip(feature.properties.Kota, { permanent: true, direction: 'right' });
    return cm;
  }

  
  var map = new L.Map("map");
  var baselayers = {};
  var bounds = null;
  if(typeof decimal_digit == "undefined") decimal_digit = 2;

  baselayer.forEach(function(layer) {
    var mapData; //= L.geoJson(layer.data, { style: getStyle, onEachFeature: getOnEachFeature });
    
    if (layer.type == "geojson") { 
      var layer_options = { style: getStyle };
      if (map_options.popup_info) layer_options["onEachFeature"] = getOnEachFeature;

      mapData = L.geoJson(layer.data, layer_options); 
    }

    if (layer.type == "raster") {
      var mapData = L.imageOverlay(layerPath, bounds, {opacity: 1});
      //NOTES: raster bound can be different with geojson data. Need to ask the image creator about the bound
    }

    if (layer.baseBound) bounds = mapData.getBounds();
    if (layer.addtoMap) mapData.addTo(map);
    if (layer.addtoControl) baselayers[layer.title] = mapData;
    layer.layer = mapData;
  })

  var show_overlay = true;
  if (typeof map_options.show_overlay != "undefined") show_overlay = map_options.show_overlay;

  //City district layer
  var grp = L.layerGroup();
  if(show_overlay) {
    $.getJSON(geojson_city_url,function(data){
      var layer = L.geoJson(data,{pointToLayer: onPointToLayer});
      grp.addLayer(layer);
    });
    grp.addTo(map);
  }

  //Road layer
  if(show_overlay) {
    var grp2 = L.layerGroup();
    $.getJSON(geojson_road_url,function(data){
      var layer = L.geoJson(data,{ weight: 1, color: road_color});
      grp2.addLayer(layer);
    });
    grp2.addTo(map);
  }

  if(bounds != null)  { map.fitBounds(bounds); /* map.setZoom(map.getZoom() + 0.5);*/ }
  if(bounds == null) baselayers = null;

  var overlayMaps = (show_overlay) ? { "Road": grp2, "Cities": grp } : null;
  var layerControls = L.control.layers( baselayers, overlayMaps, { position:"topright" } ).addTo(map);

  var sidebar;
  if (map_options.sidebar) {
    sidebar = L.control.sidebar('sidebar', { position: 'right', buttonIcon: button_icon });
    map.addControl(sidebar);
    //sidebar.show();
  }

  if (map_options.legend) {
    var legend_options = { 
        range_value: range_value, 
        range_color: range_color, 
        header_template: header_legend_template, 
        header_data: header_legend_data,
        buttonIcon: legend_icon
    };
    var legend = L.control.legend(legend_options);
    map.addControl(legend);
  }

  if (map_options.popup_info) {
    var info = L.control({ position: "topleft" });
    info.onAdd = getInfoOnAdd;
    info.update = getInfoOnUpdate;
    info.addTo(map);
  }

  map.on('baselayerchange',function(baselayer){ 
    // console.log("change");
    if(show_overlay) if(grp2._map != null) grp2.eachLayer(function (layer) { layer.bringToFront(); });
  });

  $(map).trigger("baselayerchange");
  $(map).trigger("baselayerchange");

  if (map_options.sidebar) {
    L.DomEvent.on(layerControls._container, "mouseover", function() {
      L.DomUtil.setOpacity(sidebar._openbutton,0);
    })

    L.DomEvent.on(layerControls._container, "mouseout", function() {
      L.DomUtil.setOpacity(sidebar._openbutton,1);
    });
  }

//leaflet control hack!!!
//problem when combining leaflet and materialize css
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
