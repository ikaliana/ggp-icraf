from django.shortcuts import render
import numpy as np
import pygeoj as pg
from django.conf import settings

# Create your views here.
def index(request):
	#return render(request, 'history_index.html', {})
	return lulc(request)

def driver(request):
	return render(request, 'history_driver.html', {})

def carbon_emission(request, period = None):
	return process_carbon(request, period, "history_carbon_emission.html", "e", "RATE")

def carbon_sequestration(request, period = None):
	return process_carbon(request, period, "history_carbon_sequestration.html", "s", "RATE")

def carbon_peat(request, period = None):
	return process_carbon(request, period, "history_carbon_peat.html", "p", "DATA")

def biodiversity_teci(request):
	return render(request, 'history_biodiversity_teci.html', {})

def biodiversity_difa(request):
	return render(request, 'history_biodiversity_difa.html', {})

def hydrology_sedimentasi(request):
	return render(request, 'history_hydrology_sedimentasi.html', {})

def hydrology_runoff(request):
	return render(request, 'history_hydrology_runoff.html', {})

def economic_regional(request):
	return render(request, 'history_economic_regional.html', {})

def economic_profitability(request):
	return render(request, 'history_economic_profitability.html', {})

# def market(request):
# 	return render(request, 'history_market.html', {})

# def issue(request):
# 	return render(request, 'history_issue.html', {})

def lulc(request,landcover = None,period = None):
	import datasets as ds
	ds.LoadRawData()
	ds.LoadPeriod()

	# lc_name = "Select landcover" if request.LANGUAGE_CODE == "en" else "Pilih tutupan lahan"
	landcover_list = np.append({"value": "","name_en": "Select landcover","name_id": "Pilih tutupan lahan"},ds.LANDCOVER)
	period_list = np.append([""],ds.PERIOD_LIST)
	
	if landcover == None:
		landcover_name = "Land cover" if request.LANGUAGE_CODE == "en" else "Tutupan lahan"
		ds.CalculateArea("","")
		# print("yg ini kosong")
	else:
		landcover_name = landcover_list[next(index for (index, d) in enumerate(landcover_list) if d["value"] == landcover)]["name_" + request.LANGUAGE_CODE]
		ds.CalculateArea(landcover,period)
		# print("--> " + landcover + " -- " + period)

	periods = ["",""] if (landcover == None) else period.split("-")
 
	#generate geojson data
	geojson_data1 = pg.load(filepath=settings.BASE_DIR + "/main/static/data/geojson/batas_admin.geojson")
	geojson_data2 = pg.load(filepath=settings.BASE_DIR + "/main/static/data/geojson/batas_admin.geojson") 

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

	#return render(request, request.LANGUAGE_CODE +'_history_lulc.html', context)
	return render(request, 'history_lulc.html', context)

def process_carbon(request, period, template, carbon_type, map_field):
	import datasets as ds
	ds.LoadRawData()
	ds.LoadPeriod()

	period_list = np.append([""],ds.PERIOD_LIST)

	if period == None:
		ds.CalculateDataEnv("",carbon_type)
	else:
		ds.CalculateDataEnv(period,carbon_type)


	map_data = ds.PEAT_DATA_ADMIN if carbon_type == "p" else ds.DATA_DISTRICT
	
	geojson_data1 = pg.load(filepath=settings.BASE_DIR + "/main/static/data/geojson/batas_admin.geojson")
	for feat in geojson_data1:
		nama_kec = feat.properties["KABKOTA"]
		if nama_kec in map_data.index:
			feat.properties["DATA"] =  map_data.loc[nama_kec][map_field]
		else:
			feat.properties["DATA"] =  -1

	stat_data = {}
	if carbon_type != "p":
		stat_data["total"] = round(ds.TOTAL_DATA / 1000.00, 2)
		stat_data["rate"] = round(ds.TOTAL_RATE, 4)
		stat_data["max_district"] = ds.DATA_DISTRICT_MAX_DATA
		stat_data["min_district"] = ds.DATA_DISTRICT_MIN_DATA
		stat_data["fast_district"] = ds.DATA_DISTRICT_MAX_RATE

	context = { 
		'period': period_list
		,'selected_period': period
		,'map_data1': geojson_data1
	}

	if carbon_type == "p":
		context["peat_data1"] = ds.PEAT_DATA_ADMIN if period == None else ds.PEAT_DATA_ADMIN.sort_values("DATA",ascending=False)
		context["peat_data2"] = ds.PEAT_DATA_ZONE if period == None else ds.PEAT_DATA_ZONE.sort_values("DATA",ascending=False)
	else:
		main_index = [] if period == None else ds.DATA_PERIOD_PEAT.index.get_level_values(level=0).unique()
		sub_index = [] if period == None else ds.DATA_PERIOD_PEAT.index.get_level_values(level=1).unique()

		period_data = []
		for idx in main_index:
			item = {"label": idx, "data": ds.DATA_PERIOD_PEAT.loc[idx]}
			period_data.append(item)

		context["stat_data"] = stat_data
		context["peat_data"] = ds.DATA_PERIOD
		context["peat_period_index"] = main_index
		context["peat_period_sub_index"] = sub_index
		context["peat_period_data"] = period_data
		context["district_data"] = ds.DATA_DISTRICT_TOP
		context["zone_data"] = ds.DATA_ZONE_TOP

	return render(request, template, context)

