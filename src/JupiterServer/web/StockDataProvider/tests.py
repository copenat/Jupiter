from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

class PortfolioTest(APITestCase):
    fixtures = ['test.json']

    def test_get_all_portfolios(self):
        response = self.client.get('/portfolio/?format=json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistant_portfolio(self):
        response = self.client.get('/portfolio/doesntexist/?format=json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_delete_portfolio(self):
        prtf = 'testportfolio1'
        payload = {'description': "my first portfolio", "format": "json"}
        response = self.client.post('/portfolio/{0}/'.format(prtf), data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/portfolio/{0}/?format=json'.format(prtf))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['name'], prtf)
        self.assertEquals(response.data['description'], payload['description'])

        response = self.client.delete('/portfolio/{0}/?format=json'.format(prtf))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_del_stock_to_portfolio(self):
        prtf = 'testportfolio1'
        stock = 'ARM'
        payload = {'description': "my first portfolio", "format": "json"}
        response = self.client.post('/portfolio/{0}/'.format(prtf), data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payload = {'description': "my first stock", "format": "json"}
        response = self.client.post('/stock/{0}/'.format(stock), data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/portfolio/{0}/stock/{1}/'.format(prtf, stock))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/portfolio/{0}/?format=json'.format(prtf))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)



class StockTest(APITestCase):
    fixtures = ['test.json']

    def test_get_all_stocks(self):
        response = self.client.get('/stock/?format=json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistant_stock(self):
        response = self.client.get('/stock/doesntexist/?format=json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_delete_portfolio(self):
        symbol = 'teststock'
        payload = {'description': "my first stock", "format": "json"}
        response = self.client.post('/stock/{0}/'.format(symbol), data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/stock/{0}/?format=json'.format(symbol))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['symbol'], symbol)
        self.assertEquals(response.data['description'], payload['description'])

        response = self.client.delete('/stock/{0}/?format=json'.format(symbol))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


