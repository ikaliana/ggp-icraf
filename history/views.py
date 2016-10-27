from django.shortcuts import render
import datasets as ds
import numpy as np
#from django.templatetags.static import static
#from django.http import HttpResponse

# Create your views here.
def index(request):
	return render(request, 'history_index.html', {})

def lulc(request,commodity_name):
	ds.LoadRawData()
	#ds.LoadKabupaten()
	ds.LoadPeriod()

	commodity = np.append({"value": "","name": "Select commodity"},ds.COMMODITY)
	period = np.append([""],ds.PERIOD_LIST)
	com_name = commodity[next(index for (index, d) in enumerate(commodity) if d["value"] == commodity_name)]["name"]
	if commodity_name == "":
		com_name = "&nbsp;"

	if commodity_name != "":
		ds.LoadAreaPerCommodityGroupPeriod(commodity_name)


	context = { 
		'commodity_name': com_name
		,'commodity_value': commodity_name
		,'commodity': commodity
		,'period': period
		,'com_period_data': ds.COMMODITY_AREA_GROUP_PERIOD
	}

	return render(request, 'history_lulc.html', context)

def test(request):
	return render(request,"blank.html", {})

	# csvPath = 'static/data/Historical_analysis.csv'
	# csvPath = "./main/" + csvPath
	# staticPath = static(csvPath)

	# output = ""
	# output = output + "<p>csvPath : %s</p>" % csvPath
	# output = output + "<p>staticPath : %s</p>" % staticPath
	# output = output + "<p>basename csv : %s</p>" % os.path.basename(csvPath)
	# output = output + "<p>realpath csv : %s</p>" % os.path.realpath(csvPath)
	# output = output + "<p>realpath static : %s</p>" % os.path.realpath(staticPath)
	# output = output + "<p>__file__ : %s</p>" % __file__
	# output = output + "<p>__file__ : %s</p>" % os.path.abspath(__file__)

	# return HttpResponse(output)