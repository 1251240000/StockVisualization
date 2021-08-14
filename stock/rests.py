from rest_framework import serializers

from stock.models import StockBasic


class StockBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockBasic
        fields = '__all__'


