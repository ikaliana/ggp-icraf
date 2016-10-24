from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'about_index.html', {})

def approaches(request):
	return render(request, 'about_approaches.html', {})

def planning(request):
	return render(request, 'about_planning.html', {})