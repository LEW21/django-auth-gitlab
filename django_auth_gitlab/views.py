from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect, resolve_url
from django.urls import reverse
from django.utils.http import is_safe_url

from . import oidc

def login(request):
    return_path = request.GET.get(auth.REDIRECT_FIELD_NAME, "")

    return redirect(oidc.server.authorize(
        redirect_uri = request.build_absolute_uri(reverse("django_auth_gitlab:callback")),
        state = return_path,
    ))

def callback(request):
    return_path = request.GET.get("state")

    res = oidc.server.request_token(
        redirect_uri = request.build_absolute_uri(reverse("django_auth_gitlab:callback")),
        code = request.GET["code"],
    )

    User = auth.get_user_model()
    user, created = User.objects.get_or_create(username=res.id["sub"])
    auth.login(request, user)

    url_is_safe = is_safe_url(
        url = return_path,
        host = request.get_host(),
        #allowed_hosts = set(request.get_host()),
        #require_https = request.is_secure(),
    )
    if not url_is_safe:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))
    return redirect(return_path)
