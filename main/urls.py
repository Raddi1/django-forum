from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.main_page, name='home_page'),
  path("themes/", views.ThemeListView.as_view(), name="theme-list"),
  path("themes/add/", views.ThemeCreateView.as_view(), name="theme-add"),
  path("themes/<int:pk>/edit/", views.ThemeUpdateView.as_view(), name="theme-edit"),
  path("themes/<int:pk>/delete/", views.ThemeDeleteView.as_view(), name="theme-delete"),
  path('ban/', views.ban_page, name='ban_page'),
  path('root/', views.root_page, name='root_page'),
]