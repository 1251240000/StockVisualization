from django.core.management.base import BaseCommand

from stock.models import StockBasic, StockTop10
from utils.api import tushare
from utils.formatdate import Fdate


class Command(BaseCommand):
    help = 'Update StockTop10 from tushare api'

    def handle(self, *args, **kwargs):
        StockTop10.objects.all().delete()

        df = tushare.pro.daily()

        # 取最后的交易日数据
        last_trade_date = max(df['trade_date'])
        df = df.loc[df['trade_date'] == last_trade_date]

        # 以涨幅排序
        df = df.sort_values('pct_chg')

        # 取前 10 及后 10 条记录
        for perf, iterator in zip(
            ('low', 'high'), (df[:10].iterrows(), df[-10:].iterrows())
        ):
            for _, row in iterator:
                try:
                    stock = StockBasic.objects.get(tscode=row.ts_code)
                    attrs = row.drop(['ts_code', 'pct_chg', 'change']).to_dict()

                    attrs['trade_date'] = Fdate(attrs.pop('trade_date')).Y_m_d
                    attrs['volume'] = attrs.pop('vol')

                    attrs['volume'] *= 100
                    attrs['amount'] *= 1000

                    StockTop10.objects.update_or_create(
                        stock=stock,
                        performance=perf,
                        defaults=attrs, )
                except StockBasic.DoesNotExist:
                    continue
