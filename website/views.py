from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return render(request, 'website/index.html')

def about(request):
	return render(request, 'website/about.html')

def contact(request):
	return render(request, 'website/contact.html')

def properties(request):
	return render(request, 'website/properties.html')

def partners(request):
	return render(request, 'website/partners.html')

def privacy(request):
        return render(request, 'website/privacy.html')

def terms(request):
        return render(request, 'website/terms.html')
