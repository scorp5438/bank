from rest_framework import serializers

from wallet.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'



class UpdateWalletSerializer(serializers.ModelSerializer):
    class Meta(WalletSerializer.Meta):
        fields = 'balance',

    def update(self, instance, validated_data):
        instance.balance = validated_data.get('balance', instance.balance) # TODO добавить в тест валидацию A valid number is required.AND Ensure this value is greater than or equal to 0.
        instance.save()
        return instance
