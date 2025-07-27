from django.shortcuts import render
from .models import User, BanUser, Category, Comment, Thread

# Create your views here.
def main_page(request):
  return render(request, 'main/index.html')

def ban_page(request):
    if not request.user.is_authenticated:
        return render(request, 'main/error_page.html')
    try:
        BanUser.objects.get(user=request.user)
    except BanUser.DoesNotExist:
        return render(request, 'main/error_page.html')

    return render(request, 'main/ban_page.html')