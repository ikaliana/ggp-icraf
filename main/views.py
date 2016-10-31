from django.shortcuts import render
from django.http import HttpResponse
#from .models import *
from django.templatetags.static import static
import pandas as p
import os
import pygeoj as pg

# Create your views here.
def index(request):
	return render(request, 'index.html', {})

def testgeojson(request):
	data = "./main/static/data/sample2.geojson"
	#data = "/static/data/sample1.geojson"
	datafile = pg.load(filepath=data)

	for feat in datafile:
		nama_kec = feat.properties["KABKOTA"]
		feat.properties["data"]= nama_kec + "_10"

	context = { 
		'json_data': datafile
	}

	return render(request, 'geojson.html', context)

def testcsv(request):
	csvPath = './main/static/data/Historical_analysis.csv'
	csvPath = "./main/static/data/sample1.geojson"
	#staticPath = "D:\Indra\GGP\WebApp\main\static\data\Historical_analysis.csv" #static(csvPath)
	staticPath = static(csvPath)

	#df = p.read_csv(staticPath)
	#df1 = df.query("LC_T1 == 'Grass '")
	#df2 = p.DataFrame(df1.groupby("PERIOD")["COUNT"].sum().reset_index(name="COUNT_AREA"))

	#output = "<p># %s</p>" % "TEST"
	#output = ""
	#for i in range(len(df2)):
	#	output = output + "<p>Period%s: %s</p>" %((i+1),df2.iloc[i]["PERIOD"])
	#output = df2.to_json()

	output = ""
	output = output + "<p>csvPath : %s</p>" % csvPath
	output = output + "<p>staticPath : %s</p>" % staticPath
	output = output + "<p>basename csv : %s</p>" % os.path.basename(csvPath)
	output = output + "<p>realpath csv : %s</p>" % os.path.realpath(csvPath)
	output = output + "<p>realpath static : %s</p>" % os.path.realpath(staticPath)
	output = output + "<p>__file__ : %s</p>" % __file__
	output = output + "<p>__file__ : %s</p>" % os.path.abspath(__file__)

	return HttpResponse(output)

	#return render(request, "blank.html", {})