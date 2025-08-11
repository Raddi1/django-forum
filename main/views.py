from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, BanUser, Category, Comment, Thread, User
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import RegisterForm

class ThemeListView(ListView):
    model = Thread
    template_name = "main/themes/theme_list.html"
    context_object_name = "themes"

class ThemeCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    fields = ["title", "content", "category"]
    template_name = "main/themes/theme_form.html"
    success_url = reverse_lazy("theme-list")

    def form_valid(self, form):
        form.instance.author = self.request.user  # set author automatically
        if not form.instance.category_id:
            default_category, created = Category.objects.get_or_create(title="General")
            form.instance.category = default_category
        return super().form_valid(form)


class ThemeUpdateView(UpdateView):
    model = Thread
    fields = ["title", "content"]
    template_name = "main/themes/theme_form.html"
    success_url = reverse_lazy("theme-list")

class ThemeDeleteView(DeleteView):
    model = Thread
    template_name = "main/themes/theme_confirm_delete.html"
    success_url = reverse_lazy("theme-list")

    def check_user(self):
        thread = self.get_object()
        return thread.author == self.request.user
    def check_failed(self):
        return render('main/error_page.html')

def theme_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    return render(request, 'main/themes/theme_detail.html', { "thread": thread })


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
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {
        'form': form
    })


    # ---- Звичайний рендер сторінок
    
def main_page(request):
    threads = Thread.objects.all()
    users = User.objects.all()
    return render(request, 'main/index.html', {
        'threads': threads,
        'users': users
    })

def rules_page(request):
    return render(request, 'main/rules.html')


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
