from django import forms
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, get_connection

class ContactForm(forms.Form):
    yourname = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(required=False,label='Your e-mail address')
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
 
 
def contact(request):
     submitted = False
     if request.method == 'POST':
         form = ContactForm(request.POST)
         if form.is_valid():
             cd = form.cleaned_data
             # assert False
             # assert False
             con = get_connection('django.core.mail.backends.console.EmailBackend')
             send_mail(
                 cd['subject'],
                 cd['message'],
                 cd.get('email', 'noreply@example.com'),
                 ['hsuyeemon.1@gmail.com'],
                 connection=con
             )
             return HttpResponseRedirect('/contact?submitted=True')
     else:
         form = ContactForm()
         if 'submitted' in request.GET:
             submitted = True
 
     return render(request, 'contact.html', {'form': form, 'submitted': submitted})