from django.http import HttpResponse
from django.urls import path
from django.contrib.auth import get_user_model
from django.utils.html import escape
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.urls import reverse

User = get_user_model()

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
@csrf_protect
def custom_admin_panel(request):
    message = ""

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")
        try:
            user = User.objects.get(pk=user_id)
            if action == "ban":
                user.is_active = False
                user.save()
                message = f"Користувач {user.username} забанений."
            elif action == "unban":
                user.is_active = True
                user.save()
                message = f"Користувач {user.username} розбанений."
            elif action == "make_admin":
                user.is_staff = True
                user.is_superuser = True
                user.save()
                message = f"Користувачу {user.username} видано адмінку."
            elif action == "delete":
                if user == request.user:
                    message = "Неможливо видалити себе."
                elif user.is_superuser and User.objects.filter(is_superuser=True).count() == 1:
                    message = "Неможливо видалити останнього суперкористувача."
                else:
                    user.delete()
                    message = "Користувача видалено."
        except User.DoesNotExist:
            message = "Користувача не знайдено."
        return redirect(f"{reverse('custom_admin_panel')}?msg={escape(message)}")

    message = request.GET.get("msg", "")
    csrf_token = get_token(request)

    users = User.objects.all()
    rows = ""
    for u in users:
        rows += f"""
        <tr>
            <td>{u.id}</td>
            <td>{escape(u.username)}</td>
            <td>{escape(u.email)}</td>
            <td>{u.is_active}</td>
            <td>{u.is_staff}</td>
            <td>{u.is_superuser}</td>
            <td>
                <form method="post" style="display:inline;">
                    <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                    <input type="hidden" name="user_id" value="{u.id}">
                    <button name="action" value="ban">Бан</button>
                    <button name="action" value="unban">Розбан</button>
                    <button name="action" value="make_admin">Адмінка</button>
                    <button name="action" value="delete" onclick="return confirm('Видалити користувача?');">Видалити</button>
                </form>
            </td>
        </tr>
        """

    html = f"""
    <html>
    <head><title>Кастомна адмінка</title></head>
    <body>
        <h1>Кастомна адмінка</h1>
        <p style="color:green;">{escape(message)}</p>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Email</th>
                <th>Активний</th>
                <th>Staff</th>
                <th>Superuser</th>
                <th>Дії</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('custom-admin/', custom_admin_panel, name='custom_admin_panel'),
]
