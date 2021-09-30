from rest_framework import serializers

from stock.models import StockBasic, StockTop10


class StockBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockBasic
        fields = '__all__'


class StockTop10Serializer(serializers.ModelSerializer):
    symbol = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    # 市净率
    pb = serializers.SerializerMethodField()    
    # 市盈率
    pe = serializers.SerializerMethodField()
    # 涨跌幅
    percent_change = serializers.SerializerMethodField()
    # 换手率
    turn_over_ratio = serializers.SerializerMethodField()

    def get_symbol(_, obj): return obj.stock.symbol
    def get_name(_, obj): return obj.stock.name
    def get_pb(_, obj): return obj.stock.pb
    def get_pe(_, obj): return obj.stock.pe
    def get_percent_change(_, obj): return obj.close / obj.pre_close - 1
    def get_turn_over_ratio(_, obj): 
        if obj.stock.totals:
            return obj.volume / obj.stock.totals
        return None
    class Meta:
        model = StockTop10
        fields = '__all__'