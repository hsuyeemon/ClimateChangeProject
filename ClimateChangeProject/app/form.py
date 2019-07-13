from django import forms
from django.forms import ModelForm
from .models import Country
 
class TemperatureForm(ModelForm):
      required_css_class = 'required'
      class Meta:
          model = Temperature
          fields = ['temperature','date','country']

