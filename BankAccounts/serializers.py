from rest_framework import serializers
from core.models import BankAccount

class BankAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankAccount
        fields = ['id', 'account_number', 'balance', 'customer', 'account_type', 'closed', 'has_loan', 'created_at', 'updated_at']
        read_only_fields = ['has_loan', 'closed']

    def create(self, validated_data):
        validated_data['has_loan'] = False  # Default value for has_loan
        validated_data['closed'] = False  # Default value for closed
        bank_account = BankAccount.objects.create(**validated_data)
        return bank_account

    def update(self, instance, validated_data):
        instance.account_number = validated_data.get('account_number', instance.account_number)
        instance.balance = validated_data.get('balance', instance.balance)
        instance.account_type = validated_data.get('account_type', instance.account_type)
        instance.closed = validated_data.get('closed',
                                             instance.closed)  # Allow closing of the account through serializer
        instance.has_loan = validated_data.get('has_loan', instance.has_loan)  # Update loan status if needed
        instance.save()
        return instance
