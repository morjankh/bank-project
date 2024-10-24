from rest_framework import serializers
from core.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'transaction_type', 'amount', 'fee', 'timestamp']
