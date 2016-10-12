from django.shortcuts import render
from django.http import HttpResponse
#from .models import *
from django.templatetags.static import static
import pandas as p

# Create your views here.
def index(request):
	return render(request, 'index.html', {})

def testcsv(request):
	csvPath = 'data/Historical_analysis.csv'
	staticPath = "D:\Indra\GGP\WebApp\main\static\data\Historical_analysis.csv" #static(csvPath)

	df = p.read_csv(staticPath)
	df1 = df.query("LC_T1 == 'Grass '")
	df2 = p.DataFrame(df1.groupby("PERIOD")["COUNT"].sum().reset_index(name="COUNT_AREA"))

	#output = "<p># %s</p>" % "TEST"
	#output = ""
	#for i in range(len(df2)):
	#	output = output + "<p>Period%s: %s</p>" %((i+1),df2.iloc[i]["PERIOD"])
	output = df2.to_json()

	return HttpResponse(output)

	#return render(request, "blank.html", {})