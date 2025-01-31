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
        print(validated_data)
        instance.balance = validated_data.get('balance', instance.balance)
        instance.save()
        return instance
