from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

'''
    clerks  -- User "is_staff"

    manager -- Superuser

'''

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

# class LoginForm():

#     class Meta:
#         model = 