from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.main_page, name='home_page'),
  path('ban/', views.ban_page, name='ban_page')

]