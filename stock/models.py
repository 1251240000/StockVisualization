from django import db
from django.db import models

# Create your models here.
class StockBasic(models.Model):
    tscode = models.CharField("TS股票代码", primary_key=True, db_index=True, max_length=9)
    sinacode = models.CharField("SINA股票代码", unique=True, db_index=True, max_length=8)
    symbol = models.CharField("股票代码", db_index=True, max_length=6)
    name = models.CharField("股票名称", max_length=16)
    industry = models.CharField("所属行业", max_length=16)
    area = models.CharField("地域", max_length=16)
    market = models.CharField("市场类型", max_length=16)
    list_date = models.DateField("上市日期", )

    update_date = models.DateTimeField("更新日期", auto_now=True)
    pb = models.FloatField("市净率", default=0)
    pe = models.FloatField("市盈率", default=0)
    esp = models.FloatField("每股收益", default=0)
    bvps = models.FloatField("每股净资", default=0)
    totals = models.FloatField("总股本", default=0)
    outstanding = models.FloatField("流通股本", default=0)
    total_assets = models.FloatField("总资产", default=0)
    liquid_assets = models.FloatField("流通资产", default=0)