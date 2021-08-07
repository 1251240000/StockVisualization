from django.core.management.base import BaseCommand

from stock.models import StockBasic
from utils.api import tushare
from utils.formatdate import Fdate

def _stock_code_convert(tscode):
    return ''.join(tscode.lower().split('.')[::-1])

class Command(BaseCommand):
    help = 'Update StockBasic list from api'
    maximum_bulk_length = 128

    def handle(self, *args, **kwargs):
        local_stocks = set(StockBasic.objects.values_list('tscode', flat=True))
        update_list = tushare.get_stock_list()

        stock_objects = []

        for stock_info in update_list:
            if stock_info['ts_code'] in local_stocks:
                continue

            tscode = stock_info.pop('ts_code')
            stock_info['list_date'] = Fdate(stock_info['list_date']).Y_m_d
            stock_objects.append(
                StockBasic(
                    tscode=tscode,
                    sinacode=_stock_code_convert(tscode),
                    update_date=Fdate.Y_m_d,
                    **stock_info
                )
            )
            
            if len(stock_objects) >= self.maximum_bulk_length:
                StockBasic.objects.bulk_create(stock_objects)
                stock_objects.clear()
        
        StockBasic.objects.bulk_create(stock_objects)
        