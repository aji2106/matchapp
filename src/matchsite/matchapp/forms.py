from django import forms
import re
from django.forms import ModelChoiceField
from django.db import models




class UserRegForm(forms.Form):


        username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
            "placeholder":"Username",
            "pattern":"[[^A-Za-z0-9]{3,15}",
            "name":"username",
            "title":"Usernames must be between 3 and 15 characters. Only letters and numbers are allowed"
        }))
        password = forms.CharField(label='Password',max_length=32, widget=forms.PasswordInput(attrs={
            "placeholder":"Enter password",
            "pattern":"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",
            "name":"password",
            "title":"Password must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters"
        }))
        re_password = forms.CharField(label='Repeat Password',max_length=32, widget=forms.PasswordInput(attrs={
            "placeholder":"Repeat password",
            "name":"re_password"}))


class UserLogInForm(forms.Form):
        username = forms.CharField(label='Username', min_length=2,max_length=15, widget=forms.TextInput(attrs={
        "placeholder":"Username"}))
        password = forms.CharField(label='Password', min_length=8,max_length=32, widget=forms.PasswordInput(attrs={
        "placeholder":"Password"}))

class UserProfile(forms.Form):
        username = forms.CharField(label='Enter your username', max_length=100)
        password = forms.CharField(max_length=32, widget=forms.PasswordInput)
        re_password = forms.CharField(max_length=32, widget=forms.PasswordInput)
        email=forms.EmailField()

        SOURCE_CHOICES = [
        ('Football', 'Football'),
        ('Gym', 'Gym'),
        ('Painting', 'Painting'),
        ('Music', 'Music'),
         ]
        hobbies=models.CharField(max_length=10,choices=SOURCE_CHOICES,)
        #hobbies=forms.CharField(widget=forms.Textarea)
