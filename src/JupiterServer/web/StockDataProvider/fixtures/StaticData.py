__author__ = 'Nathan'
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jugaad.settings')
from StockDataProvider.models import *
import googlefinance

techstocks = {'ARM': 'ARM Technologies', 'AVV': 'Aveva Group', 'BA.': 'BAE SYS.', 'BET': 'Betfair Group',
            'CWC': 'Cable and Wireless', 'COLT': 'Colt Group', 'CSR': 'CSR',
             'IMG': 'Imagination Technologies', 'LRD': 'Laird', 'NANO': 'Nanoco',  'PIC': 'Pace',
            'SEPU': 'Sepura', 'SPT': 'Spirent', 'TIG': 'Innovation Group',}
retailstocks= {'DEB': 'Debenhams', 'HFD': 'Halfords', 'HOME': 'Home Retail Group','MRW': 'WM Morrison',
         'MKS': 'Marks and Spenser', 'NXT': 'Next',   'PLND': 'Poundland', 'SBRY': 'Sainsburys', 'SPD': 'Sports Direct',
         'SMWH': 'WH Smith', 'TSCO': 'Tesco',
         }

def exist_or_blank(e):
    try:
        return e
    except Exception as a:
        return ""

for stock in list(techstocks.keys())+list(retailstocks.keys()):
    try:
        sd = googlefinance.getQuotes(stock)[0]

        sa = StockActivity(symbol=stock,
                           index=exist_or_blank(sd['Index']),
                          lasttradedatetime=exist_or_blank(sd['LastTradeDateTimeLong']),
                          lasttradeprice=exist_or_blank(sd['LastTradePrice']),
                          lasttradewithcurrency=exist_or_blank(sd['LastTradeWithCurrency']),
                          stockid=exist_or_blank(sd['ID']))
        sa.save()
        if stock in techstocks:
            d = techstocks[stock]
        if stock in retailstocks:
            d = retailstocks[stock]
        s = Stock(symbol=stock, description=d)
        s.latestactivity = sa
        s.save()
    except Exception as e:
        print("Could not get prices for symbol {0} {1}".format(stock, e))


p = Portfolio(name="LdnTech", description="List of my London tech stocks")
p.save()
for s in techstocks.keys():
    stock = Stock.objects.get(symbol=s)
    p.stocks.add(stock)
    p.save()

p = Portfolio(name="LdnRetail", description="List of my London retail stocks")
p.save()
for s in retailstocks.keys():
    stock = Stock.objects.get(symbol=s)
    p.stocks.add(stock)
    p.save()

