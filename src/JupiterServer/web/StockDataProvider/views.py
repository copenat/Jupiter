from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from StockDataProvider.serializers import *
import googlefinance
import logging
logger = logging.getLogger(__name__)


class PortfolioList(APIView):
    def get(self, request, format=None):
        try:
            logger.debug("Get all portfolio")
            portfolios = Portfolio.objects.all().order_by('name')
            serializer = PortfolioSerializer(portfolios, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Portfolio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class PortfolioDetail(APIView):
    def get_stock_prices(self, stocks):
        for stock in stocks.all():
            try:
                sd = googlefinance.getQuotes(stock.symbol)[0]
                logger.debug(sd)
                sa = StockActivity(symbol=stock.symbol, index=self._exist_or_blank(sd['Index']),
                          lasttradedatetime=self._exist_or_blank(sd['LastTradeDateTimeLong']),
                          lasttradeprice=self._exist_or_blank(sd['LastTradePrice']),
                          lasttradewithcurrency=self._exist_or_blank(sd['LastTradeWithCurrency']),
                          stockid=self._exist_or_blank(sd['ID']))
                sa.save()
                stock.latestactivity = sa
                stock.save()
            except Exception as e:
                logger.info("Could not get prices for symbol {0} {1}".format(stock.symbol, e))

    def _exist_or_blank(self, e):
        try:
            return e
        except Exception as a:
            return ""

    def get(self, request, portfolio, format=None):
        try:
            prtf = Portfolio.objects.get(name=portfolio)
        except Portfolio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.get_stock_prices(prtf.stocks)
        serializer = PortfolioSerializer(prtf)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, portfolio, format=None):
        try:
            prtf = Portfolio.objects.get(name=portfolio[0:99])
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Portfolio.DoesNotExist:
            try:
                portfolio_desc = request.DATA['description'][0:249]
            except :
                portfolio_desc = ''
            try:
                prtf = Portfolio(name=portfolio[0:99], description=portfolio_desc)
                prtf.save()
                return Response(status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.debug(e)

    def delete(self, request, portfolio, format=None):
        try:
            portfolio = Portfolio.objects.get(name=portfolio[0:99])
            portfolio.delete()
            return Response(status=status.HTTP_200_OK)
        except Portfolio.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PortfolioStock(APIView):
    def post(self, request, portfolio, stock, format=None):
        try:
            prtf = Portfolio.objects.get(name=portfolio[0:99])
            stock = Stock.objects.get(symbol=stock)
            prtf.stocks.add(stock)
            return Response(status=status.HTTP_200_OK)
        except (Portfolio.DoesNotExist, Stock.DoesNotExist):
            logger.debug("Could not find {0} {1}".format(portfolio, stock))
            return Response(status=status.HTTP_404_NOT_FOUND)

class StockList(APIView):
    def get(self, request, format=None):
        try:
            stocks = Stock.objects.all()
            serializer = StockSerializer(stocks, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Stock.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class StockDetail(APIView):
    def get(self, request, stock, format=None):
        try:
            stk = Stock.objects.get(symbol=stock)
            serializer = StockSerializer(stk)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Stock.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, stock, format=None):
        try:
            stk = Stock.objects.get(symbol=stock[0:99])
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Stock.DoesNotExist:
            try:
                stock_desc = request.DATA['description'][0:249]
            except :
                stock_desc = ''
            try:
                stk = Stock(symbol=stock[0:99], description=stock_desc)

                stk_act = StockActivity.objects.filter(symbol=stock[0:99]).order_by('-creation')
                if stk_act:
                    stk.latestactivity = stk_act[0]

                stk.save()
                return Response(status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.debug(e)

    def delete(self, request, stock, format=None):
        try:
            stk = Stock.objects.get(symbol=stock[0:99])
            stk.delete()
            return Response(status=status.HTTP_200_OK)
        except Stock.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
