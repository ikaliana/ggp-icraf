from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.templatetags.static import static

# Create your views here.
def index(request):
	return render(request, 'index.html', {})

def testcsv(request):
	csvPath = 'data/Historical_analysis.csv'
	#csvPath = 'css/materialize.css'
	staticPath = "D:\Indra\GGP\WebApp\main\static\data\Historical_analysis.csv" #static(csvPath)
	#resolvePath = resolve(csvPath)
	test = HistoryCsv.import_from_filename(staticPath)
	#test = HistoryCsv.import_data(data = open(staticPath))

	output = "<p># %s</p>" % HistoryCsv.has_class_delimiter() #staticPath
	return HttpResponse(output)

	#return render(request, "blank.html", {})