from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User, BanUser, Category, Comment, Thread, User
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import RegisterForm



class ThemeListView(ListView):
    model = Thread
    template_name = "main/theme_list.html"
    context_object_name = "themes"

class ThemeCreateView(CreateView):
    model = Thread
    fields = ["title", "content"]
    template_name = "main/theme_form.html"
    success_url = reverse_lazy("theme-list")

class ThemeUpdateView(UpdateView):
    model = Thread
    fields = ["title", "content"]
    template_name = "main/theme_form.html"
    success_url = reverse_lazy("theme-list")

class ThemeDeleteView(DeleteView):
    model = Thread
    template_name = "main/theme_confirm_delete.html"
    success_url = reverse_lazy("theme-list")




    # ---- Всі дії із логіном, реєстрацією і т.д

def logout_page(request):
    logout(request)
    return redirect('home_page')


def register_page(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home_page')
        else:
            return HttpResponse("Invalid form submission")
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {
        'form': form
    })


    # ---- Звичайний рендер сторінок
    
def main_page(request):
    return render(request, 'main/index.html')


def root_page(request):
    return render(request, 'main/admin/admin.html')


def ban_page(request):
    if not request.user.is_authenticated:
        return render(request, 'main/error_page.html')
    try:
        BanUser.objects.get(user=request.user)
    except BanUser.DoesNotExist:
        return render(request, 'main/error_page.html')

    return render(request, 'main/ban_page.html')


def error_page(request, exception=None):
    return render(request, 'main/error_page.html', status=500)
