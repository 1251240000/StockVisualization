from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('pick/', views.pick, name='pick'),
    path('pick/inner', views.pick_inner, name='pick_inner'),
    path('hold/', views.hold, name='hold'),
    path('predict/', views.predict, name='predict'),
    path('profile/', views.profile, name='profile')
]


handler404 = 'views.page_not_found'
