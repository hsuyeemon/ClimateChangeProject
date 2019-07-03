from django.db import models

# Create your models here.
from neomodel import StructuredNode, StringProperty, DateProperty

class Book(StructuredNode):
	title = StringProperty(unique_index=True)
	published = DateProperty()