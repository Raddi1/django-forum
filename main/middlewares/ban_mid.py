from django.shortcuts import redirect
from django.urls import reverse
from main.models import BanUser 
from django.core.exceptions import ObjectDoesNotExist

class CheckBanMiddleware:
  def __init__(self, get_response):
        self.get_response = get_response

  def __call__(self, request):
    if not request.user.is_authenticated or request.path == reverse('ban_page'):
            return self.get_response(request)
    try:
            BanUser.objects.get(user=request.user)
            return redirect('ban_page')
    except BanUser.DoesNotExist:
            pass
    
    # -----  Тут потрібно писати код який виконається ДО views.py, та наступного 

    response = self.get_response(request)

    # -----  Тут потрібно писати код який виконається ПІСЛЯ views.py