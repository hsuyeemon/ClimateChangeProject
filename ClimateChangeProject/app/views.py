from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from .models import Country
from .models import Temperature
from .models import Year
from .form import TemperatureForm
from .models import Admin
from .form import AdminForm
from neomodel import db
import json
from datetime import datetime


# Include the `fusioncharts.py` file which has required functions to embed the charts in html page
from .fusioncharts import FusionCharts

# Loading Data from a Static JSON String
# The `chart` method is defined to load chart data from an JSON string.


def index(request):

	return render(request, 'index.html')
	
    #return HttpResponse("Hello, world. You're at the polls index.")


def login(request):

	submitted = False
	if request.method == 'POST':
		form=AdminForm(request.POST)
		inputdata = request.POST.copy()
		name = inputdata.get('username')
		pwd = inputdata.get('password')
		admin_data=Admin.nodes.get(username='admin')
		db_name=admin_data.username
		db_pwd=admin_data.password
		print(db)
		if name==db_name and pwd==db_pwd:
			request.session['username'] = name
			return HttpResponseRedirect('/admin/')
			#return render(request,"/admin/")
			#return HttpResponse(request.session['username'])
			#return HttpResponse("session created!")
		else:
			return HttpResponseRedirect('/login/?submitted=False')
	else:
		form = Admin()
		if 'submitted' in request.GET:
			submitted = True

	return render(request,"login.html")

def admin(request):

	if request.session['username'] == "admin":
		return render(request,"admin.html",{'countries':load_countries()})
	else:
		return HttpResponseRedirect('/login/?submitted=False')

def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect('/login/?submitted=False')


def add_temperature(request):

	submitted = False
	if request.method == 'POST':
		form = TemperatureForm(request.POST)
		if form.is_valid():
			#form.save()
			print(form.data)
			temperature = form.data['temperature']
			print(temperature)
			date = form.data['date']
			dt = datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y')
			print(dt)
			country = form.data['country']
			#country = "Myanmar"
			y = date[0:4]
			if date[5]=="0" :
				m = date[6:7] 
			else:
				m=date[5:7]
			if date[8]=="0" :
				d = date[9] 
			else:
				d=date[8:9]	

			check_year = "WITH "+y+" as y MATCH (year : Year{value:y}) RETURN year;"
			yy,meta = db.cypher_query(check_year)


			if len(yy)!= 0:
				results = add_query(y,d,m,temperature,dt,country)
				if len(results)!=0:
					return HttpResponseRedirect('/add_temperature/?submitted=True')

				
			else:
				#//Create Time Tree with new year
				q1 = "WITH "+y+" AS year, range(1,12) AS months CREATE (y:Year {value: year}) FOREACH(month IN months | CREATE (m:Month {value: month}) MERGE (y)-[:CONTAINS]->(m))"
				db.cypher_query(q1)

				#Connect Years Sequentially
				q2 = "MATCH (year:Year) WITH year ORDER BY year.value WITH collect(year) AS years FOREACH(i in RANGE(0, length(years)-2) |     FOREACH(year1 in [years[i]] |         FOREACH(year2 in [years[i+1]] | CREATE UNIQUE (year1)-[:NEXT]->(year2))));"
				db.cypher_query(q2)

				#Connect Months Sequentially
				q3 = "MATCH (year:Year)-[:CONTAINS]->(month) WITH year, month ORDER BY year.value, month.value WITH collect(month) AS months FOREACH(i in RANGE(0, length(months)-2) | FOREACH(month1 in [months[i]] | FOREACH(month2 in [months[i+1]] |CREATE UNIQUE (month1)-[:NEXT]->(month2))));"
				db.cypher_query(q3)

				results = add_query(y,d,m,temperature,dt,country)
				if len(results)!=0:
					return HttpResponseRedirect('/add_temperature/?submitted=True')

	else:
		form = Temperature()
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 'admin.html', {'countries':load_countries(),' form': form,'submitted': submitted})
	#return HttpResponse("add_temperature")

def add_query(y,d,m,temperature,date,country):
	query = "WITH "+y+" as y MATCH (year : Year{value:y}) WITH year,"+m+" AS m MATCH (year)-[:CONTAINS]->(month:Month {value:m}) WITH year,month,"+d+" AS d CREATE (day:Day {value : d}) MERGE (month)-[:CONTAINS]->(day) WITH year,month,day,"+temperature+" as t,'"+date+"' AS date,'"+country+"' AS c CREATE (temp:Avg_temperature{Date :date,country : c,Temperature :t }) MERGE (country:Country {name: c}) MERGE (temp)-[:TEMP_OF]->(country) MERGE (temp)-[:TEMP_AT]->(day) RETURN year,month,day,temp,country"
	results,meta = db.cypher_query(query)
	return results

def get_temperature(date,country):
	
	query = "WITH '"+country+"' as c MATCH (country :Country) where country.name=c WITH country,'"+date+"' as d MATCH (tem :Avg_temperature) where tem.Date = d WITH country,tem MATCH (tem)-[r:TEMP_OF]->(country) RETURN tem.Temperature"
	results,meta = db.cypher_query(query)
	return results[0][0]



def update_temperature(request):
	updated = False
	if request.method == 'POST':
		data = request.POST.copy()
		print(data)
		date = data.get('in-datetime')
		dt = datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y')
			
		country = data.get('country')

		if data.get('temperature') != "":
			print("update")

			query = "WITH '"+country+"' as c MATCH (country :Country) where country.name=c WITH country,'"+dt+"' as d MATCH (tem :Avg_temperature) where tem.Date = d WITH country,tem MATCH (tem)-[r:TEMP_OF]->(country) SET tem.Temperature= "+str(data.get('new_temperature'))+" RETURN tem"
			results,meta = db.cypher_query(query)
			return HttpResponseRedirect('/update_temperature/?updated=True')



		else :
			result = get_temperature(dt,country)
			query = "WITH '"+country+"' as c MATCH (country :Country) where country.name=c WITH country,'"+dt+"' as d MATCH (tem :Avg_temperature) where tem.Date = d WITH country,tem MATCH (tem)-[r:TEMP_OF]->(country) RETURN tem.Temperature"
			results,meta = db.cypher_query(query)
			return render(request,'admin.html', {'countries':load_countries(),'country':country,'date':date,'old_temperature':result})

	else:
		if 'updated' in request.GET:
			updated = True
	return render(request, 'admin.html', {'countries':load_countries(),'updated': updated})
	

def delete_temperature(request):

	deleted = False
	if request.method == 'POST':
		data = request.POST.copy()
		print(data)
		date = data.get('de_datetime')
		dt = datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y')
			
		country = data.get('de_country')


		if data.get('de_temp') != "":
			print("delete")

			y = date[0:4]
			if date[5]=="0" :
				m = date[6:7] 
			else:
				m=date[5:7]
			if date[8]=="0" :
				d = date[9] 
			else:
				d=date[8:9]	

			query = "WITH toInteger("+y+") as y MATCH (year:Year {value: y}) WITH year,toInteger("+m+") as m MATCH (year)-[:CONTAINS]->(month:Month {value: m}) WITH year,month,toInteger("+d+") as d MATCH (month)-[:CONTAINS]->(day:Day{value:d}) WITH year,month,day,'"+country+"' as c Match p = (country:Country{name:c})<-[r1:TEMP_OF*]-(n:Avg_temperature)-[r2:TEMP_AT]->(day)<-[r3:CONTAINS*]-(month)<-[:CONTAINS*]-(year) WITH p,r1,r2,r3,c,n,month,day FOREACH (rel IN r1| DELETE rel) DELETE r2 FOREACH (rel IN r3| DELETE rel) DELETE n DELETE day"
			results,meta = db.cypher_query(query)
			print(results)
			return HttpResponseRedirect('/delete_temperature/?deleted=True')



		else :
			print("Else")
			result = get_temperature(dt,country)
			query = "WITH '"+country+"' as c MATCH (country :Country) where country.name=c WITH country,'"+dt+"' as d MATCH (tem :Avg_temperature) where tem.Date = d WITH country,tem MATCH (tem)-[r:TEMP_OF]->(country) RETURN tem.Temperature"
			results,meta = db.cypher_query(query)
			return render(request,'admin.html', {'countries':load_countries(),'de_country':country,'de_datetime':date,'de_temp':result})

	else:
		if 'deleted' in request.GET:
			deleted = True
	return render(request, 'admin.html', {'countries':load_countries(),'deleted': deleted})

def charts(request):
	#print(request)
	submitted = False
	global line,column2d
	if request.method == 'POST':
		data = request.POST.copy()

		if data.get('chart-type') == "line":

		#print(data.get('in-datetime1'))
			#country = data.get('country')
			country = "Myanmar" 
			year1 = int(data.get('in-year1'))
			year2 = int(data.get('in-year2'))
			data,caption,subCaption = prepare_linechart(country,year1,year2)
			line = generate_chart("line","Chart-1","chart-1",caption,subCaption,"Years",data)

			return render(request, 'charts.html', {'countries':load_countries(),'years':load_years(),'output1' : line.render(),'output2' : column2d.render()})

		else :
			year = data.get('year')
			data,caption,subCaption = prepare_column2d(year)

			#params(type,name,width,height,chart id, data type)
			column2d = generate_chart("column2d","Chart-2","chart-2",caption,subCaption,"Countries",data)
			#print(column2d)
			return render(request, 'charts.html', {'countries':load_countries(),'years':load_years(),'output1' : line.render(),'output2' : column2d.render()})
	else:
		#form = Country()
		if 'submitted' in request.GET:
			submitted = True

		data,caption,subCaption = prepare_linechart()
		line = generate_chart("line","Chart-1","chart-1",caption,subCaption,"Years",data)
		#print(load_years())
		data,caption,subCaption = prepare_column2d()
		#params(type,name,width,height,chart id, data type)
		column2d = generate_chart("column2d","Chart-2","chart-2",caption,subCaption,"Countries",data)
		return render(request, 'charts.html', {'countries':load_countries(),'years':load_years(),'output1' : line.render(),'output2' : column2d.render()})


def generate_chart(ctype,chart_name,chart_id,caption,subCaption,x_axis,data):

	chart = FusionCharts(ctype,chart_name, "100%", "400",chart_id, "json",
    
    # The data is passed as a string in the `dataSource` as parameter.
                        """{
                            "chart": {
                                "caption": '"""+caption +"""',
                                "subCaption" : '"""+subCaption+"""',
                                "showValues":"1",
                                "showPercentInTooltip" : "0",
                                "numberSuffix" : " \N{DEGREE SIGN}C",
                                "enableMultiSlicing":"0",
                                "theme": "fusion",
                                "exportEnabled" : "1",
                                "showLabels": "1" ,
                                "labelDisplay": "rotate",
        						"slantLabel": "1",
        						"xAxisName": '"""+x_axis+"""',
        						"yAxisName": "Temperature {br}(In celsius)" 
                            },
                            "data": """+ data +"""}""") 
	return chart

def prepare_column2d(year=2012):


	query = "MATCH (c:Country) WITH collect(c) AS countries UNWIND countries as country MATCH(y:Year{value:toInteger("+str(year)+")})-[:CONTAINS]->(m:Month)-[:CONTAINS]->(d:Day)<-[:TEMP_AT*]-(t:Avg_temperature)-[:TEMP_OF]->(country) WITH round(100*avg(toInteger(t.Temperature)))/100 as tavg,country RETURN {label:country.name,value:tavg}"
	results,meta = db.cypher_query(query)
	#print("column2d",results)
	
	map_list = []
	for r in results:
		map_list.append(r[0])

	country_tavg_map = json.dumps(map_list)

	caption = "Temperature Situations of All Asean Countries"
	subCaption = "From the year "+str(year)
	
	return country_tavg_map,caption,subCaption

def prepare_linechart(country="Myanmar",year1 = 1999,year2 = 2013):
	query = "MATCH (year:Year) WHERE year.value>=toInteger("+str(year1)+") AND year.value<=toInteger("+str(year2)+") WITH collect(year) AS years UNWIND years as y MATCH (y)-[:CONTAINS]->(m:Month) WITH y,m MATCH (m)-[:CONTAINS]->(d:Day) WITH y,m,d MATCH (c:Country) WHERE c.name = '"+country+"' WITH y,m,d,c MATCH (d)<-[:TEMP_AT*]-(t:Avg_temperature)-[:TEMP_OF]->(c) WITH t.Temperature as temperature,y.value as year RETURN year,toInteger(temperature)"
	results,meta = db.cypher_query(query)
	

	map_list = []
	for i in range(year1,year2+1):
		c=0
		t=0
		dic={}
		for j in range(len(results)):
			if results[j][0] == i:
				c=c+1	
				t = t + results[j][1]
			
		if c!=0:
			t = round(100*t/c)/100
			dic['label']=str(i)
			dic['value']=t
			map_list.append(dic)

	year_tavg_map = json.dumps(map_list)
	caption = "Temperature Situations of "+country
	subCaption = "From the year "+str(year1)+" to "+str(year2)

	return year_tavg_map,caption,subCaption



def load_countries():
   	#countries = Country.objects.filter(country_id=country_id).order_by('name')
    #return render(request, 'hr/city_dropdown_list_options.html', {'cities': cities})

    countries = Country.nodes.order_by('name')
    return countries
    #return render(request,'charts.html',{'countries':countries})

def load_years():

	years = Year.nodes.order_by('value')
	print(years)
	return years