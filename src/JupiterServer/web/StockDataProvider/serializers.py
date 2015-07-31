__author__ = 'Nathan'

from rest_framework import serializers
from StockDataProvider.models import *

class StockActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockActivity
        fields = ('index', 'lasttradedatetime', 'lasttradeprice', 'lasttradewithcurrency', 'stockid')

class StockSerializer(serializers.ModelSerializer):
    latestactivity = StockActivitySerializer()
    class Meta:
        model = Stock
        fields = ('symbol', 'description', 'latestactivity')

class PortfolioSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(many=True)
    class Meta:
        model = Portfolio
        fields = ('name', 'description', 'stocks')





