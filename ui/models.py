from django.db import models

class StockBasic(models.Model):
    code = models.CharField(primary_key=True,max_length=10)
    name = models.CharField(max_length=10)
    industry = models.CharField(max_length=10)
    area = models.CharField(max_length=10)
    pb = models.CharField(max_length=10)
    pe = models.CharField(max_length=10)
    esp = models.CharField(max_length=10)
    bvps = models.CharField(max_length=10)
    totals = models.CharField(max_length=10)
    outstanding = models.CharField(max_length=10)
    totalAssets = models.CharField(max_length=10)
    liquidAssets = models.CharField(max_length=10)

class StockRank(models.Model):
    code = models.CharField(primary_key=True,max_length=10)
    name = models.CharField(max_length=10)
    changepercent = models.CharField(max_length=10)
    trade = models.CharField(max_length=10)
    open = models.CharField(max_length=10)
    high = models.CharField(max_length=10)
    low = models.CharField(max_length=10)
    settlement = models.CharField(max_length=10)
    volume = models.CharField(max_length=10)
    turnoverratio = models.CharField(max_length=10)
    amount = models.CharField(max_length=10)
    per = models.CharField(max_length=10)
    pb = models.CharField(max_length=10)
    mktcap = models.CharField(max_length=10)
    nmc = models.CharField(max_length=10)

class UserInfo(models.Model):
    name = models.CharField(max_length=10, default="用户")
    passwd = models.CharField(max_length=16, null=True)
    auth = models.CharField(max_length=1, default='5')
    email = models.CharField(max_length=32, null=True)
    phone = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=10, null=True)
    createtime = models.DateField(auto_now_add=True)
    verifycode = models.CharField(max_length=6, default="000000")
    verifydeadline = models.CharField(max_length=10, default="0")
    selfstocks = models.TextField(null=True, default="sh;sz;cyb;hs300;zxb")
    selfrecords = models.TextField(null=True)
    
class MajorNews(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField(null=True)
    pubtime = models.CharField(max_length=24)
    src = models.CharField(max_length=10)

class Records(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    bprice = models.CharField(max_length=10)
    bvolume = models.CharField(max_length=10)
    btime = models.DateField(auto_now_add=True)
    issold = models.BooleanField(default=False)
    aprice = models.CharField(max_length=10, null=True)



