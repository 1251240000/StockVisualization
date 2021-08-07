from django.urls import path, include
from . import views

urlpatterns = [
    path('get_csrf_token', views.get_csrf_token),
    path('login', views.user_login),
    path('logout', views.user_logout),
]