from django.test import TestCase
from django.urls import reverse

from .models import Wallet


class WalletApiViewTestCase(TestCase):

    def setUp(self):
        self.wallet = Wallet.objects.create(
            balance='1000.10'
        )
        self.wallet2 = Wallet.objects.create(
            balance='500.49'
        )

    def tearDown(self):
        Wallet.objects.all().delete()

    def test_count_wallets(self):
        response = self.client.get(reverse('wallets:wallets-list'))
        json_data = response.json()
        self.assertEqual(len(json_data), 2)

    def test_wallet_balance(self):
        response = self.client.get(reverse('wallets:wallets-detail', kwargs={'pk': self.wallet.pk}))
        balance_test = response.json().get('balance')
        self.assertEqual(self.wallet.balance, balance_test)

    def test_create_wallet(self):
        data = {
            'balance': '100.40'
        }

        response = self.client.post(reverse('wallets:wallets-list'), data, format='json')
        json_data = response.json()
        self.assertEqual(json_data.get('balance'), data.get('balance'))


    def test_create_wallet_invalid_balance(self):
        data = {
            'balance': '-100'
        }
        valid_response = {'balance': ['Ensure this value is greater than or equal to 0.']}
        response = self.client.post(reverse('wallets:wallets-list'), data, format='json')
        json_data = response.json()
        self.assertEqual(json_data, valid_response)