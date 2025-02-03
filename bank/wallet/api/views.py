import time
from decimal import Decimal, InvalidOperation

from django.db import transaction, OperationalError
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import WalletSerializer, UpdateWalletSerializer
from ..models import Wallet


class WalletApiView(viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all().order_by('pk')
    http_method_names = ['get', 'post']


class UpdateWalletApiView(viewsets.ViewSet):
    serializer_class = UpdateWalletSerializer
    queryset = Wallet.objects.all()
    http_method_names = ['patch']

    def update(self, request, pk=None):
        operation_type = request.data.get('operationType')
        amount = request.data.get('amount')
        wallet = self.get_wallet_with_retries(pk)

        try:
            amount = Decimal(amount)
        except (ValueError, TypeError, InvalidOperation):
            return Response({"error": "Сумма должна быть числом."}, status=400)

        if amount < 0:
            return Response({"error": "Сумма должна быть положительной."}, status=400)

        if wallet is None:
            return Response({"error": "Кошелек не найден."}, status=404)

        with transaction.atomic():
            wallet.refresh_from_db()

            if operation_type == 'DEPOSIT':
                wallet.balance += amount

            elif operation_type == 'WITHDRAW':
                if wallet.balance >= amount:
                    wallet.balance -= amount

                else:
                    return Response({"error": "На балансе не достаточно средств."}, status=400)

            else:
                return Response({"error": "Некорректные данные: operationType должен быть 'DEPOSIT' или 'WITHDRAW'."},
                                status=400)

            wallet.save()

        return Response({"message": f"баланс кошелька {pk} успешно изменен. Текущий баланс {wallet.balance}"},
                            status=202)

    @transaction.atomic
    def get_wallet_with_retries(self, wallet_id, retries=3, delay=1):
        for attempt in range(retries):
            try:
                return Wallet.objects.select_for_update().get(id=wallet_id)
            except Wallet.DoesNotExist:
                return None
            except OperationalError:
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    raise
