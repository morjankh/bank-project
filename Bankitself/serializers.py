from rest_framework import serializers
from core.models import Bank

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['balance']
