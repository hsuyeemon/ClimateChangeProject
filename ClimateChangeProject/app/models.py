from django.db import models

# Create your models here.
from neomodel import config,StructuredNode, StringProperty, DateProperty,IntegerProperty
from django_neomodel import DjangoNode
from neomodel import db

class Country(DjangoNode):
	#cid = UniqueIdProperty()
	name = StringProperty()

	class Meta:
    		app_label = 'app'


class Temperature(DjangoNode):
	
	temperature = StringProperty()
	date = DateProperty()
	country = StringProperty()

	class Meta:
			app_label = 'app'
		

class Year(DjangoNode):

	value = IntegerProperty();

class Month(DjangoNode):

	value = IntegerProperty();

class Day(DjangoNode):

	value = IntegerProperty();



