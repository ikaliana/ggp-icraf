from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'di_index.html', {})

def drivers(request):
	return render(request, 'di_drivers.html', {})

def landuse(request):
	return render(request, 'di_landuse.html', {})

def env_carbon(request):
	return render(request, 'di_env_carbon.html', {})

def env_biodiversity(request):
	return render(request, 'di_env_biodiversity.html', {})

def env_hydrology(request):
	return render(request, 'di_env_hydrology.html', {})

def eco_regional(request):
	return render(request, 'di_eco_regional.html', {})

def eco_profit(request):
	return render(request, 'di_eco_profit.html', {})

def suitability(request):
	return render(request, 'di_suitability.html', {})

def hcv(request):
	return render(request, 'di_hcv.html', {})

def hcs(request):
	return render(request, 'di_hcs.html', {})

def dev_plan(request):
	return render(request, 'di_dev_plan.html', {})

# def land_requirement(request):
# 	return render(request, 'di_land_req.html', {})

# def rtrw(request):
# 	return render(request, 'di_rtrw.html', {})

# def ccm(request):
# 	return render(request, 'di_ccm.html', {})

# def lrp(request):
# 	return render(request, 'di_lrp.html', {})