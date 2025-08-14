from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.urls import path
from django.utils.html import escape
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from main.models import BanUser

User = get_user_model()

@csrf_exempt
def custom_admin_panel(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponse("Доступ заблоковано", status=403)

    message = ""
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")
        reason = request.POST.get("reason", "").strip()

        try:
            user = User.objects.get(pk=user_id)

            if action == "ban":
                user.is_active = False
                user.save()
                BanUser.objects.create(user=user, reason=reason or "Без причини")
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
                user.delete()
                message = "Користувач видалений."

        except User.DoesNotExist:
            message = "Користувача не знайдено."

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
                    <input type="hidden" name="user_id" value="{u.id}">
                    <input type="text" name="reason" placeholder="Причина бану">
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
        <table border="1" cellpadding="5">
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
    path("custom-admin/", custom_admin_panel, name="custom_admin_panel"),
]
