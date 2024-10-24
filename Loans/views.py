from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from core.models import Loans
from .serializers import GrantLoanSerializer, RepayLoanSerializer, LoanListSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loans.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'grant_loan':
            return GrantLoanSerializer
        elif self.action == 'repay':
            return RepayLoanSerializer
        elif self.action == 'customer_loans':
            return LoanListSerializer
        return super().get_serializer_class()

    @extend_schema(tags=['Loans'])
    @action(detail=False, methods=['post'], url_path='grant')
    def grant_loan(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            loan = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=['Loans'])
    @action(detail=True, methods=['post'], url_path='repay')
    def repay(self, request, pk=None):
        loan = self.get_object()
        serializer = RepayLoanSerializer(data=request.data, context={'loan_instance': loan})

        if serializer.is_valid():
            serializer.update(loan, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Endpoint to get loans for the authenticated customer
    @extend_schema(tags=['Loans'])
    @action(detail=False, methods=['get'], url_path='customer')
    def customer_loans(self, request):
        customer = request.user
        loans = Loans.objects.filter(customer=customer)
        serializer = self.get_serializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
