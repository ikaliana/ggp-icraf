from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'mt_index.html', {})

def carbon(request):
	return render(request, 'mt_carbon.html', {})

def biodiversity(request):
	return render(request, 'mt_biodiversity.html', {})

def hydrology(request):
	return render(request, 'mt_hydrology.html', {})

def lulc(request):
	return render(request, 'mt_lulc.html', {})

def economic(request):
	return render(request, 'mt_economic.html', {})

def lup(request):
	return render(request, 'mt_lup.html', {})