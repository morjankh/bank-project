from rest_framework import serializers
from core.models import Loans
from django.utils import timezone
from datetime import timedelta

class GrantLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loans
        fields = ['account', 'amount']

    def create(self, validated_data):
        request = self.context['request']
        customer = request.user

        # Create the loan
        loan = Loans.objects.create(
            customer=customer,
            account=validated_data['account'],
            amount=validated_data['amount'],
            remaining_balance=validated_data['amount'],
            due_date=timezone.now().date() + timedelta(days=365)
        )

        loan.grant_loan()
        return loan


class RepayLoanSerializer(serializers.Serializer):
    repayment_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_repayment_amount(self, value):
        """ Ensure the repayment amount is positive. """
        if value <= 0:
            raise serializers.ValidationError("Repayment amount must be greater than zero.")
        return value

    def validate(self, data):
        """ Validate repayment amount against expected monthly payment. """
        loan_instance = self.context['loan_instance']
        repayment_amount = data.get('repayment_amount')


        monthly_repayment = (loan_instance.amount * loan_instance.interest_rate) / 100


        if repayment_amount != monthly_repayment:
            raise serializers.ValidationError(f"Expected repayment is {monthly_repayment}, but received {repayment_amount}.")

        return data

    def update(self, instance, validated_data):
        repayment_amount = validated_data.get('repayment_amount')

        instance.repay(repayment_amount)

        return instance


class LoanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loans
        fields = ['id', 'account', 'amount', 'remaining_balance', 'due_date', 'paid_off', 'months']
