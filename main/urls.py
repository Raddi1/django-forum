from django.urls import path, include
from . import views, ThemeListView, ThemeCreateView, ThemeUpdateView, ThemeDeleteView

urlpatterns = [
  path('', views.main_page, name='home_page'),
  path("themes/", ThemeListView.as_view(), name="theme-list"),
  path("themes/add/", ThemeCreateView.as_view(), name="theme-add"),
  path("themes/<int:pk>/edit/", ThemeUpdateView.as_view(), name="theme-edit"),
  path("themes/<int:pk>/delete/", ThemeDeleteView.as_view(), name="theme-delete"),
  path('ban/', views.ban_page, name='ban_page')
]