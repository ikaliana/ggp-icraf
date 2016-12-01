from django.shortcuts import render
import numpy as np
import pygeoj as pg
#from django.templatetags.static import static
#from django.http import HttpResponse

# Create your views here.
def index(request):
	#return render(request, 'history_index.html', {})
	return lulc(request)

def driver(request):
	return render(request, 'history_driver.html', {})

def carbon_emission(request, period = None):
	import datasets as ds
	ds.LoadRawData()
	ds.LoadPeriod()

	period_list = np.append([""],ds.PERIOD_LIST)

	if period == None:
		ds.CalculateDataEnv("","e")
	else:
		ds.CalculateDataEnv(period,"e")

	geojson_data1 = pg.load(filepath="./main/static/data/geojson/batas_admin.geojson")
	for feat in geojson_data1:
		nama_kec = feat.properties["KABKOTA"]
		if nama_kec in ds.DATA_DISTRICT.index:
			feat.properties["DATA"] =  ds.DATA_DISTRICT.loc[nama_kec]["RATE"]
		else:
			feat.properties["DATA"] =  -1
	
	main_index = ds.DATA_PERIOD_PEAT.index.get_level_values(level=0).unique()
	period_data = ds.DATA_PERIOD_PEAT
	
	stat_data = {
		'total': round(ds.TOTAL_DATA / 1000.00, 2)
		,'rate': round(ds.TOTAL_RATE, 4)
		,'max_district': ds.DATA_DISTRICT_MAX_DATA
		,'min_district': ds.DATA_DISTRICT_MIN_DATA
		,'fast_district': ds.DATA_DISTRICT_MAX_RATE
	}

	context = { 
		'period': period_list
		,'selected_period': period
		,'stat_data': stat_data
		,'map_data1': geojson_data1
		,'peat_data': ds.DATA_PERIOD
		,'peat_period_index': main_index
		,'peat_period_data': period_data
		,'district_data': ds.DATA_DISTRICT_TOP
		,'zone_data': ds.DATA_ZONE_TOP
	}

	return render(request, 'history_carbon_emission.html', context)

def carbon_sequestration(request, period = None):
	import datasets as ds
	ds.LoadRawData()
	ds.LoadPeriod()

	period_list = np.append([""],ds.PERIOD_LIST)

	if period == None:
		ds.CalculateDataEnv("","s")
	else:
		ds.CalculateDataEnv(period,"s")

	geojson_data1 = pg.load(filepath="./main/static/data/geojson/batas_admin.geojson")
	for feat in geojson_data1:
		nama_kec = feat.properties["KABKOTA"]
		if nama_kec in ds.PEAT_DATA_ADMIN.index:
			feat.properties["DATA"] =  ds.PEAT_DATA_ADMIN.loc[nama_kec]["DATA"]
		else:
			feat.properties["DATA"] =  -1
	
	context = { 
		'period': period_list
		,'selected_period': period
		,'map_data1': geojson_data1
	}

	return render(request, 'history_carbon_sequestration.html', context)

def carbon_peat(request, period = None):
	import datasets as ds
	ds.LoadRawData()
	ds.LoadPeriod()

	period_list = np.append([""],ds.PERIOD_LIST)

	if period == None:
		ds.CalculateDataEnv("","p")
	else:
		ds.CalculateDataEnv(period,"p")

	geojson_data1 = pg.load(filepath="./main/static/data/geojson/batas_admin.geojson")
	for feat in geojson_data1:
		nama_kec = feat.properties["KABKOTA"]
		if nama_kec in ds.PEAT_DATA_ADMIN.index:
			feat.properties["DATA"] =  ds.PEAT_DATA_ADMIN.loc[nama_kec]["DATA"]
		else:
			feat.properties["DATA"] =  -1
	
	context = { 
		'period': period_list
		,'selected_period': period
		,'map_data1': geojson_data1
		,'peat_data1': ds.PEAT_DATA_ADMIN if period == None else ds.PEAT_DATA_ADMIN.sort_values("DATA",ascending=False)
		,'peat_data2': ds.PEAT_DATA_ZONE if period == None else ds.PEAT_DATA_ZONE.sort_values("DATA",ascending=False)
	}

	return render(request, 'history_carbon_peat.html', context)

def biodiversity_emission(request):
	return render(request, 'history_biodiversity_emission.html', {})

def biodiversity_sequestration(request):
	return render(request, 'history_biodiversity_sequestration.html', {})

def biodiversity_peat(request):
	return render(request, 'history_biodiversity_peat.html', {})

def hydrology(request):
	return render(request, 'history_hydrology.html', {})

def economic_regional(request):
	return render(request, 'history_economic_regional.html', {})

def economic_profitability(request, period = None):
	import datasets as ds
	ds.LoadRawData()
	ds.LoadPeriod()

	context = { 
		'period': period_list
		,'selected_period': period
	}

	return render(request, 'history_economic_profitability.html', context)

def market(request):
	return render(request, 'history_market.html', {})

def issue(request):
	return render(request, 'history_issue.html', {})

def lulc(request,landcover = None,period = None):
	import datasets as ds
	ds.LoadRawData()
	ds.LoadPeriod()

	landcover_list = np.append({"value": "","name": "Select landcover"},ds.LANDCOVER)
	period_list = np.append([""],ds.PERIOD_LIST)
	
	if landcover == None:
		landcover_name = "Land cover"
		ds.CalculateArea("","")
		# print("yg ini kosong")
	else:
		landcover_name = landcover_list[next(index for (index, d) in enumerate(landcover_list) if d["value"] == landcover)]["name"]
		ds.CalculateArea(landcover,period)
		# print("--> " + landcover + " -- " + period)

	periods = ["",""] if (landcover == None) else period.split("-")
 
	#generate geojson data
	geojson_data1 = pg.load(filepath="./main/static/data/geojson/batas_admin.geojson")
	geojson_data2 = pg.load(filepath="./main/static/data/geojson/batas_admin.geojson") 

	for feat in geojson_data1:
		nama_kec = feat.properties["KABKOTA"]
		if nama_kec in ds.AREA_PERIOD_BEGIN_ADMIN.index:
			feat.properties["DATA"] =  ds.AREA_PERIOD_BEGIN_ADMIN.loc[nama_kec]["COUNT"] / 1000.00
		else:
			feat.properties["DATA"] =  -1

	for feat in geojson_data2:
		nama_kec = feat.properties["KABKOTA"]
		if nama_kec in ds.AREA_PERIOD_END_ADMIN.index:
			feat.properties["DATA"] =  ds.AREA_PERIOD_END_ADMIN.loc[nama_kec]["COUNT"] / 1000.00
		else:
			feat.properties["DATA"] =  -1

	stat_data = {
		'area1': round(ds.AREA_PERIOD_BEGIN / 1000000.00, 2)
		,'area2': round(ds.AREA_PERIOD_END / 1000000.00, 2)
		,'growth': round(ds.AREA_GROWTH,2)
		,'num_district': ds.AREA_ADMIN_TOTAL
		,'max_district': ds.AREA_ADMIN_LARGEST
		,'fast_district': ds.AREA_ADMIN_FASTEST
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
		,'landchange_plan': ds.AREA_CHANGES_PLAN
	}

	return render(request, 'history_lulc.html', context)