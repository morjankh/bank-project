from rest_framework import viewsets
from core.models import Transaction
from .serializers import TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(tags=['Transctions']),
    retrieve=extend_schema(tags=['Transctions']))
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Custom logic for transaction creation
        serializer.save()
