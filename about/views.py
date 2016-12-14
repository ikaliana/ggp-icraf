from django.shortcuts import render

# Create your views here.
def index(request):
	# request.LANGUAGE_CODE
	print request.LANGUAGE_CODE
	return render(request, request.LANGUAGE_CODE +'_about_index.html', {})

def approaches(request):
	return render(request, request.LANGUAGE_CODE +'_about_approaches.html', {})

def planning(request):
	return render(request, request.LANGUAGE_CODE +'_about_planning.html', {})