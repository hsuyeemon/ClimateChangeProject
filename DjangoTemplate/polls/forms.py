from django import forms
from django.forms import ModelForm
from .models import Venue
 
class VenueForm(ModelForm):
      required_css_class = 'required'
      class Meta:
          model = Venue
          fields = '__all__'