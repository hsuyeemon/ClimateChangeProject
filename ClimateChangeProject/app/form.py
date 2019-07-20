from django import forms
from django.forms import ModelForm
from .models import Temperature
from .models import Admin
 
class TemperatureForm(ModelForm):
      required_css_class = 'required'
      class Meta:
          model = Temperature
          fields = ['temperature','date','country']

class AdminForm(ModelForm):
    required_css_class='required'
    class Meta:
        model=Admin
        fields=['username','password']
        