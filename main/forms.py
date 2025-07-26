from django import forms
from captcha.fields import CaptchaField
from django.forms import Form, ModelForm, EmailInput, SlugField, TextInput, PasswordInput, Textarea 
from django.core.exceptions import ValidationError
from django.forms import CharField
from django.urls import reverse
from .models import User, Thread, Comment, Category

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ['content', 'parent']
    widget = {
        'content': forms.Textarea(attrs={'rows': 3}),
        'parent': forms.HiddenInput
      }