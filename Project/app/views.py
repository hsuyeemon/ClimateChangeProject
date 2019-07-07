from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from .models import Country
from .form import CountryForm


def index(request):
	return render(request, 'base.html')
	
    #return HttpResponse("Hello, world. You're at the polls index.")

def add_country(request):
     submitted = False
     if request.method == 'POST':
         form = CountryForm(request.POST)
         if form.is_valid():
             form.save()
             print("save")
             return HttpResponseRedirect('/add_country/?submitted=True')
     else:
         form = Country()
         if 'submitted' in request.GET:
             submitted = True
     return render(request, 'add_country.html', {'form': form, 'submitted': submitted})
     #return HttpResponse("DONE")

def get_country(request):
    a= [0,1,2,3]
    b= {'a':0,'b':1}
    return render( request, 'country.html',{'country': Country.nodes.all(),'list':a,'dict':b})

def delete_country(request):
    submitted = False
    if request.method == 'POST':
        aa = request.POST
        c = Country.nodes.get(name=aa.get('name'))
        c.delete();
        return HttpResponseRedirect('/delete_country/?submitted=True')

    else:
         form = Country()
         if 'submitted' in request.GET:
             submitted = True
    return render(request, 'delete_country.html', {'form': form, 'submitted': submitted})