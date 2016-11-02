from django.shortcuts import render
import datasets as ds
import numpy as np
import pygeoj as pg
#from django.templatetags.static import static
#from django.http import HttpResponse

# Create your views here.
def index(request):
	#return render(request, 'history_index.html', {})
	return lulc(request)

def environmental(request):
	return render(request, 'history_environmental.html', {})

def economic(request):
	return render(request, 'history_economic.html', {})

def market(request):
	return render(request, 'history_market.html', {})

def issue(request):
	return render(request, 'history_issue.html', {})

def lulc(request,commodity_name = None, period = None):
	ds.LoadRawData()
	ds.LoadPeriod()

	commodity = np.append({"value": "","name": "Select commodity"},ds.COMMODITY)
	period_list = np.append([""],ds.PERIOD_LIST)
	
	if commodity_name == None:
		com_name = "&nbsp;"
		ds.AreaPerCommodityAndPeriod("",period)
		max_area = 0
		min_area = 0
	else:
		com_name = commodity[next(index for (index, d) in enumerate(commodity) if d["value"] == commodity_name)]["name"]
		ds.AreaPerCommodityAndPeriod(commodity_name,period)
		max_area = ds.COMMODITY_PER_PERIOD_KAB.max()["COUNT"]
		min_area = ds.COMMODITY_PER_PERIOD_KAB.min()["COUNT"]

	#generate geojson data
	geojson_data = pg.load(filepath="./main/static/data/sample3.geojson")
	for feat in geojson_data:
		nama_kec = feat.properties["KABKOTA"]
		if nama_kec in ds.COMMODITY_PER_PERIOD_KAB.index:
			feat.properties["DATA"] =  ds.COMMODITY_PER_PERIOD_KAB.loc[nama_kec]["COUNT"]
		else:
			feat.properties["DATA"] =  0;

	context = { 
		'commodity_name': com_name
		,'commodity_value': commodity_name
		,'commodity': commodity
		,'period': period_list
		,'selected_period': period
		,'com_period_data': ds.COMMODITY_AREA_GROUP_PERIOD
		,'com_period_peat': ds.COMMODITY_PER_PERIOD_PEAT
		,'map_data': geojson_data
		,'map_max_value': max_area
		,'map_min_value': min_area
	}

	return render(request, 'history_lulc.html', context)

def test(request):
	return render(request,"blank.html", {})

	# csvPath = 'static/data/Historical_analysis.csv'
	# csvPath = "./main/" + csvPath
	# staticPath = static(csvPath)

	# output = ""
	# output = output + "<p>csvPath : %s</p>" % csvPath
	# output = output + "<p>staticPath : %s</p>" % staticPath
	# output = output + "<p>basename csv : %s</p>" % os.path.basename(csvPath)
	# output = output + "<p>realpath csv : %s</p>" % os.path.realpath(csvPath)
	# output = output + "<p>realpath static : %s</p>" % os.path.realpath(staticPath)
	# output = output + "<p>__file__ : %s</p>" % __file__
	# output = output + "<p>__file__ : %s</p>" % os.path.abspath(__file__)

	# return HttpResponse(output)