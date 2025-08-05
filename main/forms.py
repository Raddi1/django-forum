from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Comment

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['content', 'parent']
    widget = {
        'content': forms.Textarea(attrs={'rows': 3}),
        'parent': forms.HiddenInput
      }
    

class RegisterForm(UserCreationForm):

    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control',
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'class': 'form-control',
        })
    )

    password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'data-toggle': 'password',
            'id': 'password',
        })
    )

    password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control',
            'data-toggle': 'password',
            'id': 'password-confirm',
        })
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
