from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from core.models import BankAccount
from .serializers import BankAccountSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]


    @extend_schema(tags=['Bank Account'])
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Close a specific bank account if there is no outstanding loan or negative balance."""
        account = self.get_object()
        # Check if the account is already closed
        if account.closed:
            return Response({"error": "Account already closed"}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with the closure if the account is not already closed
        if account.has_loan:
            return Response({"error": "Cannot close account with an outstanding loan"},
                            status=status.HTTP_400_BAD_REQUEST)
        if account.balance < 0:
            return Response({"error": "Cannot close account with a negative balance"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Close the account
        account.close()
        return Response({"status": "Account closed successfully"}, status=status.HTTP_200_OK)
