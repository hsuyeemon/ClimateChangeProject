from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from .models import Country
#from .form import CountryForm
from neomodel import db


def index(request):
	return render(request, 'base.html')
	
    #return HttpResponse("Hello, world. You're at the polls index.")

def add_temperature(request):

	return HttpResponse("add_temperature")

def get_temperature(request):

	return HttpResponse("get_temperature")

def update_temperature(request):

	return HttpResponse("update_temperature")

def delete_temperature(request):

	return HttpResponse("delete_temperature")