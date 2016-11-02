from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'di_index.html', {})

def driver_lulc(request):
	return render(request, 'di_driver_lulc.html', {})

def environmental_services(request):
	return render(request, 'di_environmental.html', {})

def economic(request):
	return render(request, 'di_economic.html', {})

def lup(request):
	return render(request, 'di_lup.html', {})

def valuechain(request):
	return render(request, 'di_valuechain.html', {})

def land_requirement(request):
	return render(request, 'di_land_req.html', {})

def suitability(request):
	return render(request, 'di_land_sup.html', {})

def hcv(request):
	return render(request, 'di_hcv.html', {})

def rpjmd(request):
	return render(request, 'di_rpjmd.html', {})

def rtrw(request):
	return render(request, 'di_rtrw.html', {})

def ccm(request):
	return render(request, 'di_ccm.html', {})

def lrp(request):
	return render(request, 'di_lrp.html', {})