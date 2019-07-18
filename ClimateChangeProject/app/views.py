from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from .models import Country
from .models import Temperature
from .form import TemperatureForm
from neomodel import db


def index(request):

	return render(request, 'index.html')
	
    #return HttpResponse("Hello, world. You're at the polls index.")

def charts(request):

	return render(request, 'charts.html')

def login(request):

	return render(request, 'login.html')
	
    #return HttpResponse("Hello, world. You're at the polls index.")

def add_temperature(request):
	submitted = False
	count="zzz"
	if request.method == 'POST':
		form = TemperatureForm(request.POST)
		if form.is_valid():
			#form.save()
			temperature = form.data['temperature']
			date = form.data['date']
			dt = form.data['date']
			country = form.data['country']
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
				results = add_query(y,d,m,temperature,date,country)
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

				results = add_query(y,d,m,temperature,date,country)
				if len(results)!=0:
					return HttpResponseRedirect('/add_temperature/?submitted=True')

	else:
		form = Temperature()
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 'add_temperature.html', {'form': form,'submitted': submitted})
	#return HttpResponse("add_temperature")

def get_temperature(request):

	return HttpResponse("get_temperature")

def get_temperature_for_all_country(request):

	year = 2011
	query = "MATCH (c:Country) WITH collect(c) AS countries UNWIND countries as country MATCH(y:Year{value:toInteger("+str(year)+")})-[:CONTAINS]->(m:Month)-[:CONTAINS]->(d:Day)<-[:TEMP_AT*]-(t:Avg_temperature)-[:TEMP_OF]->(country) WITH avg(toInteger(t.Temperature)) as tavg,country RETURN country.name,tavg"
	results,meta = db.cypher_query(query)
	return HttpResponse(results)

def get_temperature_for_country(request):

	country = "Myanmar"
	year1 = 2010
	year2 = 2012

	query = "MATCH (year:Year) WHERE year.value>=toInteger("+str(year1)+") AND year.value<=toInteger("+str(year2)+") WITH collect(year) AS years UNWIND years as y MATCH (y)-[:CONTAINS]->(m:Month) WITH y,m MATCH (m)-[:CONTAINS]->(d:Day) WITH y,m,d MATCH (c:Country) WHERE c.name = '"+country+"' WITH y,m,d,c MATCH (d)<-[:TEMP_AT*]-(t:Avg_temperature)-[:TEMP_OF]->(c) WITH t,y RETURN toInteger(t.Temperature) as Temperature, y.value as Year" 
	results,meta = db.cypher_query(query)

	#res = []
	#for r in results:
	#	temp = 0
	#	if r[1] ==2011:
	#		temp+=r[0]
	#	res.append(temp)

	dic = dict()
	c = dict()

	for i in range(year1,year2+1):
		count = 0
		temp = 0
		for j in results:
			if j[1] == i:
				count +=1
				temp +=j[0]

		if count>0:
			dic[i] = round(temp/count,2)
		else:
			dic[i] = temp
		c[i] = count



	#return HttpResponse(dic.get(2012))
	return render(request, 'get_temperature_for_a_country.html', {'results': results,'dic':dic})
	

def update_temperature(request):

	return HttpResponse("update_temperature")

def delete_temperature(request):

	return HttpResponse("delete_temperature")

def add_query(y,d,m,temperature,date,country):
	query = "WITH "+y+" as y MATCH (year : Year{value:y}) WITH year,"+m+" AS m MATCH (year)-[:CONTAINS]->(month:Month {value:m}) WITH year,month,"+d+" AS d CREATE (day:Day {value : d}) MERGE (month)-[:CONTAINS]->(day) WITH year,month,day,"+temperature+" as t,'"+date+"' AS date,'"+country+"' AS c CREATE (temp:Avg_temperature{Date :date,country : c,Temperature :t }) MERGE (country:Country {name: c}) MERGE (temp)-[:TEMP_OF]->(country) MERGE (temp)-[:TEMP_AT]->(day) RETURN year,month,day,temp,country"
	results,meta = db.cypher_query(query)
	return results
	