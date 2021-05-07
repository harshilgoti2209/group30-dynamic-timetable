from .models import Account,Notes
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm

class UserSignUpForm(UserCreationForm):
    class Meta:
        model=Account
        fields=('username','email','batch','password1','password2')

class profileform(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    batch=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    class Meta:
        model=Account
        fields=('username','email','batch',)

class profform(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    # batch=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    class Meta:
        model=Account
        fields=('username','email',)     

class loginForm( AuthenticationForm):
    username=forms.CharField(widget=forms.EmailInput(attrs={ 'placeholder':'Email', 'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={ 'placeholder':'Password','class':'form-control'}))
    class Meta:
        model=Account
        fields=('username','password')
    
class ProfSignUpForm(UserCreationForm):
    email=forms.EmailField(max_length=70)
    class Meta:
        model=Account
        fields=('username','email','password1','password2')

class changePasswordForm(PasswordChangeForm):
    class Meta:
        model:Account
        fields=('old_password','new_password1','new_password2')

class Editnotes(forms.ModelForm):
    class Meta:
        model=Notes
        fields=('notes',)
    