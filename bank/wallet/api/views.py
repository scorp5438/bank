from decimal import Decimal, InvalidOperation

from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import WalletSerializer, UpdateWalletSerializer
from ..models import Wallet


class WalletApiView(viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    http_method_names = ['get', 'post']


class UpdateWalletApiView(viewsets.ViewSet):
    serializer_class = UpdateWalletSerializer
    queryset = Wallet.objects.all()
    http_method_names = ['patch']

    def update(self, request, pk=None):
        operationType = request.data.get('operationType')
        amount = request.data.get('amount')
        try:
            amount = Decimal(amount)
        except (ValueError, TypeError, InvalidOperation):
            return Response({"error": "Сумма должна быть числом."}, status=400)
        if amount < 0:
            return Response({"error": "Сумма должна быть положительной."}, status=400)
        wallet = self.get_wallet(pk)

        if wallet is None:
            return Response({"error": "Кошелек не найден."}, status=404)
        serializer = self.serializer_class(wallet) # TODO Узнать, надо ли оно и зачем
        if operationType == 'DEPOSIT':
            wallet.balance += amount
        elif operationType == 'WITHDRAW':
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

    def get_wallet(self, wallet_id):
        try:
            return Wallet.objects.get(id=wallet_id)
        except Wallet.DoesNotExist:
            return None
