from rest_framework import viewsets, status
from rest_framework.response import Response
from core.models import Bank
from .serializers import BankSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

class BankViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Bankiteself'])
    def retrieve_balance(self, request):
        """Retrieve the bank balance."""
        bank = Bank.objects.first()
        if bank is None:
            return Response({'error': 'Bank not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BankSerializer(bank)
        return Response(serializer.data, status=status.HTTP_200_OK)

