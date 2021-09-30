'''
Description: 
Version: 1.0.1
Autor: hrlu.cn
Date: 2021-09-30 13:33:45
LastEditors: hrlu.cn
LastEditTime: 2021-09-30 17:40:25
'''
from django import db
from django.db import models

# Create your models here.
class StockBasic(models.Model):
    tscode = models.CharField("TS股票代码", primary_key=True, db_index=True, max_length=9)
    sinacode = models.CharField("SINA股票代码", unique=True, db_index=True, max_length=8)
    symbol = models.CharField("股票代码", db_index=True, max_length=6)
    name = models.CharField("股票名称", max_length=16)
    industry = models.CharField("所属行业", max_length=16, null=True)
    area = models.CharField("地域", max_length=16, null=True)
    market = models.CharField("市场类型", max_length=16, null=True)
    list_date = models.DateField("上市日期", )

    update_date = models.DateTimeField("更新日期", auto_now=True)
    pb = models.FloatField("市净率", default=0)
    pe = models.FloatField("市盈率", default=0)
    eps = models.FloatField("每股收益", default=0)
    bvps = models.FloatField("每股净资", default=0)
    totals = models.FloatField("总股本", default=0)
    outstanding = models.FloatField("流通股本", default=0)
    total_assets = models.FloatField("总资产", default=0)
    liquid_assets = models.FloatField("流通资产", default=0)


class StockTop10(models.Model):
    PerformanceChoices = [
        ('high', "创新高"),
        ('low', "创新低"),
    ]
    stock = models.OneToOneField(StockBasic, verbose_name="股票", on_delete=models.CASCADE)
    trade_date = models.DateField("交易日期")
    performance = models.CharField("表现", choices=PerformanceChoices, max_length=4)
    pre_close = models.FloatField("昨收价", default=0)
    price = models.FloatField("当前价", default=0)
    open = models.FloatField("开盘价", default=0)
    close = models.FloatField("收盘价", default=0)
    high = models.FloatField("最高价", default=0)
    low = models.FloatField("最低价", default=0)
    volume = models.FloatField("成交量", default=0)
    amount = models.FloatField("成交额", default=0)
