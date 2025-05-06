from django import forms
from django.contrib.auth.models import User

class register_Form(forms.Form):
    name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_name(self):
        name = self.cleaned_data['name']
        if User.objects.filter(username=name).exists():
            raise forms.ValidationError("Username already taken")
        return name
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError("Password not match.")


class login_Form(forms.Form):
    name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
class playlist_Form(forms.Form):
    name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
        'placeholder' : 'e.g Happy ..'
    }))
    
