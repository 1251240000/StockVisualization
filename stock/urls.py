from django.urls import path, include
from . import views

urlpatterns = [
    path('test', views.test),
    path('stock/daily_quotation', views.daily_quotation),
    path('stock/basic', views.stock_basic),
    
]