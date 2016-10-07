from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'about_index.html', {})

def help(request):
	return render(request, 'about_help.html', {})