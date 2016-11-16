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

def lulc(request,landcover = None,period = None):
	ds.LoadRawData()
	ds.LoadPeriod()

	landcover_list = np.append({"value": "","name": "Select commodity"},ds.LANDCOVER)
	period_list = np.append([""],ds.PERIOD_LIST)
	
	if landcover == None:
		landcover_name = "&nbsp;"
		ds.CalculateArea("","")
		# print("yg ini kosong")
	else:
		landcover_name = landcover_list[next(index for (index, d) in enumerate(landcover_list) if d["value"] == landcover)]["name"]
		ds.CalculateArea(landcover,period)
		# print("--> " + landcover + " -- " + period)
 
	#generate geojson data
	geojson_data1 = pg.load(filepath="./main/static/data/geojson/batas_admin.geojson")
	geojson_data2 = pg.load(filepath="./main/static/data/geojson/batas_admin.geojson") 

	for feat in geojson_data1:
		nama_kec = feat.properties["KABKOTA"]
		if nama_kec in ds.AREA_PERIOD_BEGIN_ADMIN.index:
			feat.properties["DATA"] =  ds.AREA_PERIOD_BEGIN_ADMIN.loc[nama_kec]["COUNT"]
		else:
			feat.properties["DATA"] =  0

	for feat in geojson_data2:
		nama_kec = feat.properties["KABKOTA"]
		if nama_kec in ds.AREA_PERIOD_END_ADMIN.index:
			feat.properties["DATA"] =  ds.AREA_PERIOD_END_ADMIN.loc[nama_kec]["COUNT"]
		else:
			feat.properties["DATA"] =  0

	periods = period.split("-")
	stat_data = {
		'area1': round(ds.AREA_PERIOD_BEGIN / 1000000.00, 2)
		,'area2': round(ds.AREA_PERIOD_END / 1000000.00, 2)
		,'growth': round(ds.AREA_GROWTH,2)
		,'num_district': ds.AREA_ADMIN_TOTAL
		,'max_district': ds.AREA_ADMIN_LARGEST
		,'period1': periods[0]
		,'period2': periods[1]
	}

	context = { 
		'landcover_list': landcover_list
		,'selected_landcover': landcover
		,'period': period_list
		,'selected_period': period
		,'landcover_title': landcover_name
		,'map_data1': geojson_data1
		,'map_data2': geojson_data2
		,'stat_data': stat_data
		,'peat_data': ds.AREA_PEAT
		,'landcover_data': ds.AREA_LANDCOVER
		,'landcover_plan': ds.AREA_LANDCOVER_PLAN
		,'landchanges': ds.AREA_PERIOD
		# ,'com_period_data': ds.COMMODITY_AREA_GROUP_PERIOD
		# ,'com_period_peat': ds.COMMODITY_PER_PERIOD_PEAT
		# ,'map_max_value': max_area
		# ,'map_min_value': min_area
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