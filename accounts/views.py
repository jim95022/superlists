from django.contrib import messages, auth
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.urls import reverse

from accounts.models import Token


def send_login_email(request):
    """Отправить сообщение для входа в систему"""
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(reverse("login") + "?token=" + str(token.uid))
    message_body = f"Use this link to log in:\n\n{url}"
    send_mail(
        'Your login link for Superlists',
        message_body,
        'noreply@superlists',
        [email],
    )
    messages.success(
        request,
        "Check your email",
    )
    return redirect("/")


def login(request):
    """Зарегистрировать вход в систему"""
    auth.authenticate(uid=request.GET.get("token"))
    return redirect("/")
