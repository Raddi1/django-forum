from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator

class User(AbstractUser):
    pass

class BanUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    banned_by = models.ForeignKey(User, related_name='bans_made', on_delete=models.SET_NULL, null=True)
    reason = models.TextField()

class Category(models.Model):
    title = models.CharField(max_length=32, unique=True)

class Thread(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(null=False, validators=[MinLengthValidator(3)], max_length=80)
    content = models.TextField(null=False, validators=[MaxLengthValidator(2000)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='threads')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(validators=[MinLengthValidator(1), MaxLengthValidator(2000)])
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] 
        # Для того щоб коментарі завжди сортувались по часу

