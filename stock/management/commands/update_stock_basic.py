'''
Description: 
Version: 1.0.1
Autor: hrlu.cn
Date: 2021-09-30 17:31:11
LastEditors: hrlu.cn
LastEditTime: 2021-09-30 17:48:16
'''
from django.core.management.base import BaseCommand

from stock.models import StockBasic
from utils.api import sinajs
from utils.logger import Logger

class Command(BaseCommand):
    help = 'Update Stock Basic info from sinajs api'
    
    maximum_bulk_length = 128
    update_fields = ['pb', 'pe', 'eps', 'bvps', 'totals', 'outstanding', 
                    'total_assets', 'liquid_assets']

    def handle(self, *args, **kwargs):
        queryset = StockBasic.objects.all()    
        info_list = sinajs.get_stock_basic_in_bulk(queryset)

        stock_list = []

        for info in info_list:
            try:
                stock = queryset.get(sinacode=info['sinacode'])
                
                for attr in self.update_fields:
                    setattr(stock, attr, info[attr])

                stock_list.append(stock)

            except Exception as e:
                Logger.warning("<stock.management.commands.update_stock_basic>"
                               "Stock Basic update failed", e)

            if len(stock_list) > self.maximum_bulk_length:
                StockBasic.objects.bulk_update(stock_list, fields=self.update_fields)
                stock_list.clear()
        
        StockBasic.objects.bulk_update(stock_list, fields=self.update_fields)