from decimal import Decimal, InvalidOperation

from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import WalletSerializer, UpdateWalletSerializer
from ..models import Wallet


class WalletApiView(viewsets.ModelViewSet):
    """
    Представление для работы с кошельками (Wallet).

    Поддерживает следующие HTTP-методы:
    - GET: Получить список всех кошельков или детали конкретного кошелька.
    - POST: Создать новый кошелек.

    Атрибуты:
    - serializer_class: Сериализатор, используемый для преобразования данных.
    - queryset: Запрос для получения всех кошельков, отсортированных по первичному ключу.
    - http_method_names: Список разрешенных HTTP-методов (GET, POST).
    """
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all().order_by('pk')
    http_method_names = ['get', 'post']


class UpdateWalletApiView(viewsets.ViewSet):
    """
    Представление для выполнения операций с балансом кошелька.

    Поддерживает следующие HTTP-методы:
    - PATCH: Обновить баланс кошелька (пополнение или списание).

    Атрибуты:
    - serializer_class: Сериализатор, используемый для обновления баланса.
    - queryset: Запрос для получения всех кошельков.
    - http_method_names: Список разрешенных HTTP-методов (PATCH).

    Пример запроса:
    {
        "operationType": "WITHDRAW",
        "amount": 500
    }
    """
    serializer_class = UpdateWalletSerializer
    queryset = Wallet.objects.all()
    http_method_names = ['patch']

    def update(self, request, pk=None):
        """
        Обновляет баланс кошелька.

        Аргументы:
        - request: Запрос, содержащий данные для обновления.
        - pk: Первичный ключ кошелька, который нужно обновить.

        Логика:
        1. Проверяет, что сумма (amount) является числом и положительной.
        2. Проверяет, что тип операции (operationType) корректен (DEPOSIT или WITHDRAW).
        3. Если операция WITHDRAW, проверяет, что на балансе достаточно средств.
        4. Обновляет баланс кошелька в транзакции с использованием select_for_update
           для предотвращения race conditions.

        Возвращает:
        - В случае успеха: Сообщение об успешном изменении баланса и новый баланс.
        - В случае ошибки: Сообщение об ошибке и соответствующий HTTP-статус.
        """
        operation_type = request.data.get('operationType')
        amount = request.data.get('amount')

        try:
            amount = Decimal(amount)
        except (ValueError, TypeError, InvalidOperation):
            return Response({'error': 'The amount must be a number.'}, status=400)

        if amount < 0:
            return Response({"error": 'The amount must be positive.'}, status=400)

        if operation_type not in ['DEPOSIT', 'WITHDRAW']:
            return Response(
                {'error': 'Incorrect data: operationType must be \'DEPOSIT\' or \'WITHDRAW\'.'},
                status=400
            )

        with transaction.atomic():
            try:
                wallet = Wallet.objects.select_for_update().get(id=pk)
            except Wallet.DoesNotExist:
                wallet = None
            if wallet is None:
                return Response({'error': 'Wallet not found.'}, status=404)

            if operation_type == 'DEPOSIT':
                wallet.balance += amount
            elif operation_type == 'WITHDRAW':
                if wallet.balance < amount:
                    return Response(
                        {'error': 'There are not enough funds on the balance.'},
                        status=400
                    )
                wallet.balance -= amount

            wallet.save()

        return Response(
            {'message': f'wallet balance {pk} successfully changed. Current balance {wallet.balance}'},
            status=200
        )
