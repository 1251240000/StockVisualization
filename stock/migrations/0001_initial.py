# Generated by Django 3.1.12 on 2021-07-31 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockBasic',
            fields=[
                ('tscode', models.CharField(db_index=True, max_length=9, primary_key=True, serialize=False, verbose_name='TS股票代码')),
                ('sinacode', models.CharField(db_index=True, max_length=8, unique=True, verbose_name='SINA股票代码')),
                ('symbol', models.CharField(db_index=True, max_length=6, verbose_name='股票代码')),
                ('name', models.CharField(max_length=16, verbose_name='股票名称')),
                ('industry', models.CharField(max_length=16, verbose_name='所属行业')),
                ('area', models.CharField(max_length=16, verbose_name='地域')),
                ('market', models.CharField(max_length=16, verbose_name='市场类型')),
                ('list_date', models.DateField(verbose_name='上市日期')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('pb', models.FloatField(default=0, verbose_name='市净率')),
                ('pe', models.FloatField(default=0, verbose_name='市盈率')),
                ('esp', models.FloatField(default=0, verbose_name='每股收益')),
                ('bvps', models.FloatField(default=0, verbose_name='每股净资')),
                ('totals', models.FloatField(default=0, verbose_name='总股本')),
                ('outstanding', models.FloatField(default=0, verbose_name='流通股本')),
                ('total_assets', models.FloatField(default=0, verbose_name='总资产')),
                ('liquid_assets', models.FloatField(default=0, verbose_name='流通资产')),
            ],
        ),
    ]
