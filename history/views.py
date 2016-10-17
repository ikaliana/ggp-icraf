from django.shortcuts import render
from main import datasets as ds

# Create your views here.
def index(request):
	return render(request, 'history_index.html', {})

def lulc(request):
	ds.LoadRawData()
	ds.LoadKabupaten()
	ds.LoadPeriod()
	context = {'kab': ds.KAB_LIST, 'period': ds.PERIOD_LIST }
	return render(request, 'history_lulc.html', context)