from .models import Account,Notes
from django import forms
from django.contrib.auth.forms import UserCreationForm

class UserSignUpForm(UserCreationForm):
    email=forms.EmailField(max_length=70)
    class Meta:
        model=Account
        fields=('username','email','batch','password1','password2')

class profileform(forms.ModelForm):
    class Meta:
        model=Account
        fields=('username','email','batch',)   

class ProfSignUpForm(UserCreationForm):
    email=forms.EmailField(max_length=70)
    class Meta:
        model=Account
        fields=('username','email','password1','password2')

class Editnotes(forms.ModelForm):
    class Meta:
        model=Notes
        fields=('notes',)
    