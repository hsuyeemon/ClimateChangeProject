from django import forms
from django.forms import ModelForm
from .models import Country
 
class CountryForm(ModelForm):
      required_css_class = 'required'
      class Meta:
          model = Country
          fields = ['name']

