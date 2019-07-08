from django.db import models

# Create your models here.
from neomodel import config,StructuredNode, StringProperty, DateProperty,UniqueIdProperty
from django_neomodel import DjangoNode
from neomodel import db

#class Person(StructuredNode):
    #uid = UniqueIdProperty()
    #name = StringProperty(unique_index=True)
    #age = IntegerProperty(index=True, default=0)


#jim = Person(name='Jim', age=3).save() # Create
#jim.age = 4
#jim.save() # Update, (with validation)
#jim.delete()
#print(jim)
#jim.refresh() # reload properties from the database
#jim.id # neo4j internal id
# Return all nodes
#all_nodes = Person.nodes.all()

# Returns Person by Person.name=='Jim' or raises neomodel.DoesNotExist if no match
#jim = Person.nodes.get(name='Jim')

class Country(DjangoNode):
	#cid = UniqueIdProperty()
	name = StringProperty()

	class Meta:
    		app_label = 'app'



