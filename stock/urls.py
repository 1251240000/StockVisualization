from django.urls import path, include
from rest_framework import routers

from stock import views

router = routers.DefaultRouter()
router.register('basic', views.StockBasicViewSet)
router.register('top10', views.StockTop10ViewSet)


urlpatterns = [
    path('store/', include(router.urls)),
    path('crawl/daily_quotation', views.daily_quotation),
    path('crawl/basic', views.stock_basic),
]