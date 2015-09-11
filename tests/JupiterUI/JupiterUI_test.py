__author__ = 'Nathan'

import unittest
import logging
import configparser
from JupiterUI.lib.JupiterUI import *

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.DEBUG)

class MyPortfolioList():
    def __init__(self, url):
        pass
    def get(self):
        return ['TestA', 'TestB']

class MyPortfolioData():
    def __init__(self, url):
        pass
    def get(self, portfolio):
        return {"name": "TestA", "description": "TestA description", \
"stocks": [{"symbol": "BD32", "description": "John Lewis Partnership", \
"latestactivity": {"index": "LON", "lasttradedatetime": "Jul 16, 4:21PM GMT+1", \
"lasttradeprice": "148.50", "lasttradewithcurrency": "GBX148.50", "stockid": "9354233"}},]}

class TestJupiterUI(unittest.TestCase):
    def setUp(self):
        self.config = configparser.ConfigParser()
        self.app = None

    def tearDown(self):
        self.app.destroy()

    def testStartUp(self):
        self.app = JupiterUIApp(self.config, MyPortfolioList)
        self.assertTrue(self.app)

    def testPressGo(self):
        self.app = JupiterUIApp(self.config, MyPortfolioList)
        self.app._set_portfoliodata(MyPortfolioData)
        self.app.e.btn.invoke()

class TestPortfolioList(unittest.TestCase):
    def testPortList(self):
        l = PortfolioList("http://127.0.0.1:0000")
        self.assertTrue(l.get()[0] == "empty")

class TestPortfolioData(unittest.TestCase):
    def testPortData(self):
        d = PortfolioData("http://127.0.0.1:0000")
        self.assertTrue(d.get("test_prft") == {})


