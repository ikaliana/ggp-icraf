from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'mt_index.html', {})

def environmental(request):
	return render(request, 'mt_environmental.html', {})

def lulc(request):
	return render(request, 'mt_lulc.html', {})

def economic(request):
	return render(request, 'mt_economic.html', {})