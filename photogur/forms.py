# from django.forms import CharField, PasswordInput, Form
from photogur.models import Picture
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())


class PictureForm(forms.ModelForm):

    class Meta:
        model = Picture
        fields = ['title', 'artist', 'url']
