from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class User(models.Model):
    username = models.TextField(unique=True, null=False, min_length=3, max_length=16)
    email = models.EmailField(unique=True, null=False)
    password = models.TextField(null=False)
    is_staff = models.BooleanField(default=False)

    # Пізніше це потрібно буде доробити
    profile_image = models.ImageField() 

class Thread(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(null=False, min_length=5, max_length=80)
    content = models.TextField(null=False, max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    pass
#   Модель для коментарів буде дороблена пізніше 

class Category(models.Model):
    name = models.TextField(null=False, max_length=16)