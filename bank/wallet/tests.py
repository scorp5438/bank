from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Wallet


class WalletApiViewTestCase(TestCase):

    def setUp(self):
        wallets = [
            Wallet(balance='1000.10'),
            Wallet(balance='500.49'),
        ]
        Wallet.objects.bulk_create(wallets)

    def tearDown(self):
        Wallet.objects.all().delete()

    def test_count_wallets(self):
        response = self.client.get(reverse('wallets:wallets-list'))
        json_data = response.json()
        self.assertEqual(len(json_data), 2)


    def test_wallet_balance(self):
        wallet = Wallet.objects.filter(pk=1).first()
        response = self.client.get(reverse('wallets:wallets-detail', kwargs={'pk': wallet.pk}))
        balance_test = response.json().get('balance')
        self.assertEqual(str(wallet.balance), balance_test)

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


class UpdateWalletApiView(TestCase):

    def setUp(self):
        wallets = [
            Wallet(balance=1000.10),
            Wallet(balance=500.49),
            Wallet(balance=0.00),
        ]
        Wallet.objects.bulk_create(wallets)

    def tearDown(self):
        Wallet.objects.all().delete()

    def test_deposit_wallet(self):
        data = {
            'operationType': 'DEPOSIT',
            'amount': 1000
        }
        wallet = Wallet.objects.filter(pk=3).first()
        reference_data_text = f'баланс кошелька {wallet.pk} успешно изменен.'

        response = self.client.patch(reverse('wallets:wallet_operation', kwargs={'pk': wallet.pk}), data=data,
                                     content_type='application/json')
        wallet.refresh_from_db()
        response_data = response.json().get('message')

        self.assertEqual(response.status_code, 202)
        self.assertEqual(wallet.balance, 1000.00)
        self.assertIn(reference_data_text, response_data, msg='Ошибка, данный тест не пройден')

    def test_withdraw_wallet_valid(self):
        data = {
            'operationType': 'WITHDRAW',
            'amount': 1000
        }
        wallet = Wallet.objects.filter(pk=1).first()
        reference_data_text = f'баланс кошелька {wallet.pk} успешно изменен.'

        response = self.client.patch(reverse('wallets:wallet_operation', kwargs={'pk': wallet.pk}), data=data,
                                     content_type='application/json')

        wallet.refresh_from_db()
        response_data = response.json().get('message')

        self.assertEqual(response.status_code, 202)
        self.assertEqual(str(wallet.balance), '0.10')
        self.assertIn(reference_data_text, response_data, msg='Ошибка, данный тест не пройден')

    def test_withdraw_wallet_invalid(self):
        data = {
            'operationType': 'WITHDRAW',
            'amount': 1000
        }
        wallet = Wallet.objects.filter(pk=2).first()
        reference_data_text = 'На балансе не достаточно средств.'

        response = self.client.patch(reverse('wallets:wallet_operation', kwargs={'pk': wallet.pk}), data=data,
                                     content_type='application/json')

        wallet.refresh_from_db()
        response_data = response.json().get('error')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(str(wallet.balance), '500.49')
        self.assertEqual(reference_data_text, response_data, msg='Ошибка, данный тест не пройден')

    def test_non_existent_wallet(self):
        data = {
            'operationType': 'DEPOSIT',
            'amount': 1000
        }
        response = self.client.patch(reverse('wallets:wallet_operation', kwargs={'pk': 4}), data=data,
                                     content_type='application/json')
        reference_data_text = 'Кошелек не найден.'
        response_data = response.json().get('error')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(reference_data_text, response_data, msg='Ошибка, данный тест не пройден')

    def test_invalid_amount(self):
        data = {
            'operationType': 'DEPOSIT',
            'amount': 'one thousand'
        }

        wallet = Wallet.objects.filter(pk=3).first()
        reference_data_text = 'Сумма должна быть числом.'

        response = self.client.patch(reverse('wallets:wallet_operation', kwargs={'pk': wallet.pk}), data=data,
                                     content_type='application/json')
        response_data = response.json().get('error')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(reference_data_text, response_data, msg='Ошибка, данный тест не пройден')

    def test_invalid_operation(self):
        data = {
            'operationType': 'INVALID',
            'amount': 1000
        }

        wallet = Wallet.objects.filter(pk=3).first()
        reference_data_text = "operationType должен быть 'DEPOSIT' или 'WITHDRAW'"

        response = self.client.patch(reverse('wallets:wallet_operation', kwargs={'pk': wallet.pk}), data=data,
                                     content_type='application/json')
        response_data = response.json().get('error')

        self.assertEqual(response.status_code, 400)
        self.assertIn(reference_data_text, response_data, msg='Ошибка, данный тест не пройден')
