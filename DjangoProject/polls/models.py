from django.db import models

# Create your models here.
#from neomodel import StructuredNode, StringProperty, DateProperty
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo)

#class Book(StructuredNode):
		#title = StringProperty(unique_index=True)
		#published = DateProperty()

class Country(StructuredNode):
    code = StringProperty(unique_index=True, required=True)

class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    age = IntegerProperty(index=True, default=0)

    # traverse outgoing IS_FROM relations, inflate to Country objects
    country = RelationshipTo(Country, 'IS_FROM')

jim = Person(name='Jim', age=3).save() # Create
jim.age = 4
jim.save() # Update, (with validation)
jim.delete()
print(jim)
jim.refresh() # reload properties from the database
jim.id # neo4j internal id
# Return all nodes
all_nodes = Person.nodes.all()

# Returns Person by Person.name=='Jim' or raises neomodel.DoesNotExist if no match
jim = Person.nodes.get(name='Jim')