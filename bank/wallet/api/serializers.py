from rest_framework import serializers

from wallet.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Wallet.

    Поля:
    - id: Уникальный идентификатор кошелька.
    - balance: Текущий баланс кошелька.

    Используется для:
    - Сериализации данных кошелька при чтении (GET-запросы).
    - Десериализации данных кошелька при создании (POST-запросы).
    """
    class Meta:
        model = Wallet
        fields = '__all__'


class UpdateWalletSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления баланса кошелька.

    Наследует поля от WalletSerializer, но ограничивает доступные поля только балансом.

    Поля:
    - balance: Новое значение баланса кошелька.

    Метод `update`:
    - Обновляет баланс кошелька на основе переданных данных.
    - Возвращает обновленный экземпляр кошелька.
    """
    class Meta(WalletSerializer.Meta):
        fields = 'balance',

    def update(self, instance, validated_data):
        """
        Обновляет баланс кошелька.

        Аргументы:
        - instance: Экземпляр модели Wallet, который нужно обновить.
        - validated_data: Валидированные данные, переданные для обновления.

        Возвращает:
        - Обновленный экземпляр кошелька.
        """
        instance.balance = validated_data.get('balance', instance.balance)
        instance.save()
        return instance
