__author__ = 'Nathan'

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from StockDataProvider.views import PortfolioList, PortfolioDetail, PortfolioStock, StockList, StockDetail

urlpatterns = patterns('',

    url(r'^portfolio/$', PortfolioList.as_view()),
    url(r'^portfolio/(?P<portfolio>[_\-a-zA-Z0-9]+)/$', PortfolioDetail.as_view()),
    url(r'^portfolio/(?P<portfolio>[_\-a-zA-Z0-9]+)/stock/(?P<stock>[_\-a-zA-Z0-9]+)/$', PortfolioStock.as_view()),

    url(r'^stock/$', StockList.as_view()),
    url(r'^stock/(?P<stock>[_\-a-zA-Z0-9]+)/$', StockDetail.as_view()),

)

urlpatterns = format_suffix_patterns(urlpatterns)


