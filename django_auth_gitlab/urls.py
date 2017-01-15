from django.conf.urls import url
from . import views

app_name = 'django_auth_gitlab'
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^callback/$', views.callback, name='callback'),
]
