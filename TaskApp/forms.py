from django import forms
from .models import Employee

class LoginForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    # confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model= Employee
        fields=('email','password')
        labels = {
            'email' : 'Email',
            'password':'Password'
        }   
        
          