from django.db import models

# Create your models here.
#from neomodel import StructuredNode, StringProperty, DateProperty
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo)

#class Book(StructuredNode):
		#title = StringProperty(unique_index=True)
		#published = DateProperty()

class Venue(models.Model):
       name = models.CharField('Venue Name', max_length=120)
       address = models.CharField(max_length=300)
       zip_code = models.CharField('Zip/Post Code', max_length=12)
       phone = models.CharField('Contact Phone', max_length=20)
       web = models.URLField('Web Address')
       email_address = models.EmailField('Email Address')
   
       def __str__(self):
          return self.name