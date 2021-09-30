'''
Description: 
Version: 1.0.1
Autor: hrlu.cn
Date: 2021-09-30 13:29:05
LastEditors: hrlu.cn
LastEditTime: 2021-09-30 13:29:06
'''
from django.db.models import Q
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, action

from stock.models import StockBasic, StockTop10
from stock.rests import StockBasicSerializer, StockTop10Serializer

from utils.api import akshare, tushare, sinajs
from utils.decorators import authenticate_required, request_methods
from utils.logger import Logger
from utils.response import rest_resp, StockStdResp
from config import DEFAULT_STOCK
# Create your views here.


def _get_stock(request):
    code = request.GET.get('code', ) or DEFAULT_STOCK
    stock = StockBasic.objects.filter(
        Q(tscode=code) | Q(sinacode=code) | Q(symbol=code)
    )
    if stock.count() == 1:
        return stock.first()
    return None

@api_view()
@permission_classes((permissions.AllowAny, ))
@request_methods(['GET'])
def daily_quotation(request):
    stock = _get_stock(request)
    if stock is None:
        return StockStdResp.NotFound

    for api in (tushare, sinajs):
        try:
            return rest_resp(
                results=api.get_daily_quotation(stock)
            )
        except Exception as e:
            Logger.error("<stock.views.daily_quotation>",
                         "Daily Quotation fetching failed", e)

    return StockStdResp.Bad


@api_view()
@permission_classes((permissions.AllowAny, ))
@request_methods(['GET'])
def stock_basic(request):
    stock = _get_stock(request)
    if stock is None:
        return StockStdResp.NotFound

    for api in (sinajs, ):
        try:
            return rest_resp(
                results=api.get_stock_basic(stock)
            )
        except Exception as e:
            Logger.error("<stock.views.stock_basic>",
                         "Stock Basic fetching failed", e)

    return StockStdResp.Bad


class StockBasicViewSet(viewsets.ModelViewSet):
    queryset = StockBasic.objects.all()
    serializer_class = StockBasicSerializer
    search_fields = ['tscode', 'sinacode', 'symbol']

    @action(methods=['GET'], detail=False)
    def register(self, request):
        return rest_resp(
            results=self.queryset.values(
                # 'sinacode'
                'tscode', 'symbol', 'name'
            )
        )


class StockTop10ViewSet(viewsets.ModelViewSet):
    queryset = StockTop10.objects.all().select_related('stock')
    serializer_class = StockTop10Serializer
    filter_fields = ['performance']