from rest_framework import serializers
from core.models import BankOperation, BankAccount


# class BankOperationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BankOperation
#         fields = ['account', 'operation_typed', 'amount', 'recipient_account', 'timestamp']

# class BankAccountOperationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BankAccount
#         fields = ['account_number', 'balance']


class DepositWithdrawSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=8, decimal_places=2)
    currency_code = serializers.CharField(max_length=3, required=False)


class TransferSerializer(serializers.Serializer):
    from_account = serializers.IntegerField()
    to_account = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=8, decimal_places=2)
    currency_code = serializers.CharField(max_length=3, required=False)


