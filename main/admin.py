from django.contrib import admin
from .models import Thread

@admin.register(Thread)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")

