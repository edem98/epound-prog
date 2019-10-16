from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from myproject.apps.core.models import Account
from archive.models import ReactivationClient
from membre.models import ConsommateurParticulier, Trader
from compte.models import CompteTrader, CompteConsommateur


class CreateUserByTraderTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        # create Trader
        trader_account = CompteTrader()
        trader_account.solde = 100000
        trader_account.save()
        trader = Trader(nom="Eyadoma", prenoms="Pepe", compte_trader=trader_account, telephone="96169610")
        # send creation request
        url = 'http://127.0.0.1:8000/api/creation-particulier-trader/'
        data = {
            'numero_trader': '96169610',
            'telephone': '90178608'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Trader.objects.count(), 1)
        self.assertEqual(ConsommateurParticulier.objects.count(), 1)
        self.assertEqual(trader.compte_trader.solde, 99000)
