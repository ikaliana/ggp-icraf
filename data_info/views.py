from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'di_index.html', {})

def driver_lulc(request):
	return render(request, 'di_driver_lulc.html', {})

def environmental_services(request):
	return render(request, 'di_environmental.html', {})

def economic_impact(request):
	return render(request, 'di_economic.html', {})

def land_requirement(request):
	return render(request, 'di_land_req.html', {})

def land_supply(request):
	return render(request, 'di_land_sup.html', {})

def development_plan(request):
	return render(request, 'di_dev_plan.html', {})

def other_plan(request):
	return render(request, 'di_other_plan.html', {})