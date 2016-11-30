L.Control.legend = L.Control.extend({
	options: {
        // topright, topleft, bottomleft, bottomright
        position: "bottomleft",
        buttonIcon: "",
        header_template: "",
        header_data: {},
        item_template: "<span class='legend-item' style='background: {COLOR}'></span>{LVAL} &ndash; {RVAL}<br>",
        item_data: {},
        range_value: [],
        range_color: []
    },

    initialize: function (options) {
    	L.setOptions(this, options);

    	var container = L.DomUtil.create('div', 'legend-box open');
    	this._container = container;

    	var button = L.DomUtil.create("a", "base-panel toggle-button", container); 
        if (this.options.buttonIcon == "") button.innerHTML = "L";
        else {
            var img = L.DomUtil.create("img","",button)
            $(img).attr("src",this.options.buttonIcon);
        }
        this._togglebutton = button;

    	var panel = L.DomUtil.create("div", "base-panel card-panel card-content",container);
    	var legend_header = "";

    	if(this.options.header_template != "") {
    		legend_header = L.Util.template(this.options.header_template, this.options.header_data);
    	}

    	panel.innerHTML = legend_header + this.generateItem();

    	this._panel = panel;

	},

	generateItem: function() {
	    var maxlength = range_color.length;

	    var legend_item = "";
	    for ( i = 0; i < maxlength; i++ ) {
	      
	      var lval = (i==0) ? 0 : range_value[i-1];
	      var rval = range_value[i];
	      legend_item += L.Util.template(this.options.item_template, { COLOR: range_color[i], LVAL: lval, RVAL: rval});

	      // legend_item += "<span class='legend-item' style='background: " + range_color[i] + "'></span> ";
	      // legend_item += lval + " &ndash; ";
	      // legend_item += rval;
	      // legend_item += "<br>";
	    }	
	    
	    return legend_item;	
	},

	isVisible: function () {
        return L.DomUtil.hasClass(this._container, 'open');
    },

    show: function () {
        if (!this.isVisible()) {
            L.DomUtil.addClass(this._container, 'open');
            L.DomUtil.addClass(this._togglebutton, 'hidden');
            L.DomUtil.removeClass(this._panel, 'hidden');
        }
    },

    hide: function (e) {
        if (this.isVisible()) {
            L.DomUtil.removeClass(this._container, 'open');
            L.DomUtil.removeClass(this._togglebutton, 'hidden');
            L.DomUtil.addClass(this._panel, 'hidden');
        }
    },

	onAdd: function (map) {
		// L.DomEvent.on(this._togglebutton, 'click', this.show, this);
		// L.DomEvent.on(this._panel, 'click', this.hide, this);
        L.DomEvent.on(this._togglebutton, 'mouseover', this.show, this);
        L.DomEvent.on(this._panel, 'mouseout', this.hide, this);
		this.hide();
        console.log(this._panel)
		return this._container;
	},

	onRemove: function (map) {
		// L.DomEvent.off(this._togglebutton, 'click', this.show, this);
		// L.DomEvent.off(this._panel, 'click', this.hide, this);
        L.DomEvent.off(this._togglebutton, 'mouseover', this.show, this);
        L.DomEvent.off(this._panel, 'mouseout', this.hide, this);
	}
});

L.control.legend = function (options) {
    return new L.Control.legend(options);
};