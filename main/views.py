from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, BanUser, Comment, Thread, User
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import RegisterForm, CommentForm

class ThemeListView(ListView):
    model = Thread
    template_name = "main/themes/theme_list.html"
    context_object_name = "themes"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context

class ThemeCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    fields = ["title", "content"]
    template_name = "main/themes/theme_form.html"
    success_url = reverse_lazy("home_page")

    def form_valid(self, form):
        form.instance.author = self.request.user  # 
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
    
@login_required
def theme_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    comments = Comment.objects.filter(thread=thread)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.thread = thread
            comment.save()
            return redirect('theme-detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'main/themes/theme_detail.html', {
        "thread": thread,
        "comments": comments,
        "comment_form": form
    })


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



