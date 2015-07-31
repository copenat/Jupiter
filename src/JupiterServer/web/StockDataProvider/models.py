from django.db import models

class StockActivity(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    symbol = models.CharField(max_length=100, blank=False)
    index = models.CharField(max_length=100, blank=True)
    lasttradedatetime = models.CharField(max_length=100, blank=True)
    lasttradeprice = models.CharField(max_length=20, blank=True)
    lasttradewithcurrency = models.CharField(max_length=250, blank=True)
    stockid = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return "{0} {1} {2} {3}".format(self.id, self.symbol, self.lasttradeprice, self.lasttradedatetime)

class Stock(models.Model):
    symbol = models.CharField(primary_key=True, max_length=100, blank=False)
    description = models.CharField(max_length=250, blank=True)
    latestactivity = models.ForeignKey(StockActivity, null=True)

    def __str__(self):
        return "{0}".format(self.symbol)

class Portfolio(models.Model):
    name = models.CharField(primary_key=True, max_length=100, blank=False)
    description = models.CharField(max_length=250, blank=True)
    stocks = models.ManyToManyField(Stock)

    def __str__(self):
        return "{0}".format(self.name)
