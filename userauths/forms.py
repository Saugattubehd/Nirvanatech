from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User



class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'form-control rounded', 'placeholder': 'Full Name'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={ 'class' : 'form-control rounded', 'placeholder': 'Email'}), required=True)
    mobile = forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'form-control rounded', 'placeholder': 'Phone No.'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={ 'class' : 'form-control rounded', 'placeholder': 'Password'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={ 'class' : 'form-control rounded', 'placeholder': 'Confirm Password'}), required=True)
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'mobile', 'password1', 'password2']


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={ 'class' : 'form-control rounded', 'placeholder': 'Email'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={ 'class' : 'form-control rounded', 'placeholder': 'Password'}), required=True)
   
    class Meta:
        model = User
        fields = ['email', 'password']