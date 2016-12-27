from django.shortcuts import render
from django.conf import settings

# Create your views here.
def index(request):
	# print(settings.BASE_DIR)
	return render(request, 'index.html', {})
