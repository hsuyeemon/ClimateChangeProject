from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from datetime import date
import calendar
from calendar import HTMLCalendar
  
  
def index(request, year=date.today().year, month=date.today().month):
	year = int(year)
	month = int(month)
	if year < 1900 or year > 2099: year = date.today().year
	month_name =calendar.month_name[month]
	title = "MyClub Event Calendar - %s %s" % (month_name, year)
	cal = HTMLCalendar().formatmonth(year, month)
    #return HttpResponse("<h1>%s</h1><p>%s</p>" % (title, cal))
	#return render(request, 'base.html', {'title': title, 'cal': cal})
	return render(request, 'calendar_base.html', {'title': title, 'cal': cal})
	#return render(request, 'formEg.html', {'title': title, 'cal': cal})


from .models import Venue
from .forms import VenueForm
  
  # ...
 
def add_venue(request):
     submitted = False
     if request.method == 'POST':
         form = VenueForm(request.POST)
         if form.is_valid():
             #form.save()
             return HttpResponseRedirect('/add_venue/?submitted=True')
     else:
         form = VenueForm()
         if 'submitted' in request.GET:
             submitted = True
     return render(request, 'add_venue.html', {'form': form, 'submitted': submitted})