from django import forms
from . import models

uType=((2,'Librarian')  , (4,'VIP User') , (3 , 'Normal User'))

class LoginForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['user_id' ,  'pword']
        widgets={
            'pword':forms.PasswordInput()
        }

class SignUpForm(forms.ModelForm):
    class Meta:
        model=models.User
        exclude=['status']
        widgets={
            'uType':forms.Select(choices=uType),

        }

class BookForm(forms.ModelForm):
    class Meta:
        model=models.Book
        fields="__all__"