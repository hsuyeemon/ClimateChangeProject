from django.db import models

# Create your models here.
#from neomodel import StructuredNode, StringProperty, DateProperty
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo)

#class Book(StructuredNode):
		#title = StringProperty(unique_index=True)
		#published = DateProperty()