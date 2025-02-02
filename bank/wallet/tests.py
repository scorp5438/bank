from django.test import TestCase
from django.urls import reverse

from .models import Wallet


class WalletApiViewTestCase(TestCase):

    def setUp(self):
        self.wallet = Wallet.objects.create(balance='1000.10')
        self.wallet2 = Wallet.objects.create(balance='500.49')

    def tearDown(self):
        Wallet.objects.all().delete()

    def test_count_wallets(self):
        response = self.client.get(reverse('wallets:wallets-list'))
        json_data = response.json()
        self.assertEqual(len(json_data), 2)


    def test_wallet_balance(self):
        response = self.client.get(reverse('wallets:wallets-detail', kwargs={'pk': self.wallet.pk}))
        balance_test = response.json().get('balance')
        self.assertEqual(str(self.wallet.balance), balance_test)

    def test_create_wallet(self):
        data = {
            'balance': '100.40'
        }

        response = self.client.post(reverse('wallets:wallets-list'), data, format='json')
        json_data = response.json()
        self.assertEqual(json_data.get('balance'), data.get('balance'))
        self.assertEqual(response.status_code, 201)

    def test_create_wallet_with_balance_not_num(self):
        data = {
            'balance': 'sdf'
        }
        valid_response = 'A valid number is required.'
        response = self.client.post(reverse('wallets:wallets-list'), data, format='json')
        json_data = response.json().get('balance')

        self.assertIn(valid_response, json_data)
        self.assertEqual(response.status_code, 400)

    def test_create_wallet_invalid_balance(self):
        data = {
            'balance': '-100'
        }
        valid_response = {'balance': ['Ensure this value is greater than or equal to 0.']}
        response = self.client.post(reverse('wallets:wallets-list'), data, format='json')
        json_data = response.json()
        self.assertEqual(json_data, valid_response)
        self.assertEqual(response.status_code, 400)

class UpdateWalletApiView(TestCase):

    def setUp(self):
        self.wallet = Wallet.objects.create(balance='1000.10')
        self.wallet2 = Wallet.objects.create(balance='500.49')
        self.wallet3 = Wallet.objects.create(balance='0.00')



    def tearDown(self):
        Wallet.objects.all().delete()

    def test_deposit_wallet(self):
        data = {
            'operationType': 'DEPOSIT',
            'amount': 1000
        }

        reference_data_text = f'баланс кошелька {self.wallet3.pk} успешно изменен.'

        response = self.client.patch(reverse('wallets:wallet_operation', kwargs={'pk': self.wallet3.pk}), data=data,
                                     content_type='application/json')
        self.wallet3.refresh_from_db()
        response_data = response.json().get('message')

        self.assertEqual(response.status_code, 202)
        self.assertEqual(self.wallet3.balance, 1000.00)
        self.assertIn(reference_data_text, response_data, msg='Ошибка, данный тест не пройден')

    def test_withdraw_wallet_valid(self): # Не проходит
        data = {
            'operationType': 'WITHDRAW',
            'amount': 1000
        }
        reference_data_text = f'баланс кошелька {self.wallet.pk} успешно изменен.'

        response = self.client.patch(reverse('wallets:wallet_operation', kwargs={'pk': self.wallet.pk}), data=data,
                                     content_type='application/json')

        self.wallet.refresh_from_db()
        response_data = response.json().get('message')
        self.assertEqual(response.status_code, 202)
        self.assertEqual(str(self.wallet.balance), '0.10')
        self.assertIn(reference_data_text, response_data, msg='Ошибка, данный тест не пройден')

    def test_withdraw_wallet_invalid(self):
        data = {
            'operationType': 'WITHDRAW',
            'amount': 1000
        }
        reference_data_text = 'На балансе не достаточно средств.'

        response = self.client.patch(reverse('wallets:wallet_operation', kwargs={'pk': self.wallet2.pk}), data=data,
                                     content_type='application/json')

        self.wallet2.refresh_from_db()
        response_data = response.json().get('error')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(self.wallet2.balance), '500.49')
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

        reference_data_text = 'Сумма должна быть числом.'

        response = self.client.patch(reverse('wallets:wallet_operation', kwargs={'pk': self.wallet3.pk}), data=data,
                                     content_type='application/json')
        response_data = response.json().get('error')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(reference_data_text, response_data, msg='Ошибка, данный тест не пройден')

    def test_invalid_operation(self):
        data = {
            'operationType': 'INVALID',
            'amount': 1000
        }

        reference_data_text = "operationType должен быть 'DEPOSIT' или 'WITHDRAW'"

        response = self.client.patch(reverse('wallets:wallet_operation', kwargs={'pk': self.wallet3.pk}), data=data,
                                     content_type='application/json')
        response_data = response.json().get('error')

        self.assertEqual(response.status_code, 400)
        self.assertIn(reference_data_text, response_data, msg='Ошибка, данный тест не пройден')

    def test_update_wallet_with_positive_balance(self):
        data = {
            'operationType': 'DEPOSIT',
            'amount': -1000
        }

        reference_data_text = 'Сумма должна быть положительной.'

        response = self.client.patch(reverse('wallets:wallet_operation', kwargs={'pk': self.wallet3.pk}), data=data,
                                     content_type='application/json')
        self.wallet3.refresh_from_db()
        response_data = response.json().get('error')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.wallet3.balance, 0.0)
        self.assertIn(reference_data_text, response_data, msg='Ошибка, данный тест не пройден')