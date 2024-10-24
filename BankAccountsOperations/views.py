from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from core.models import BankAccount, BankOperation
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from .serializers import DepositWithdrawSerializer, TransferSerializer


################################################################################################
class BankOperationViewSet(viewsets.ViewSet):

    def get_object(self, pk):
        try:
            return BankAccount.objects.get(pk=pk)
        except BankAccount.DoesNotExist:
            return None


    @extend_schema(
        request=DepositWithdrawSerializer,
        responses={200: 'Deposit successful'}
    )
    @extend_schema(tags=['operations'])
    @action(detail=True, methods=['post'])
    def deposit(self, request, pk=None):
        account = self.get_object(pk)
        if account is None:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)


        serializer = DepositWithdrawSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            currency_code = serializer.validated_data.get('currency_code', 'NIS')
            try:
                account.deposit(float(amount), currency_code)
                BankOperation.objects.create(account=account, operation_type='deposit', amount=amount)
                return Response({"status": "Deposit successful"}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @extend_schema(
        request=DepositWithdrawSerializer,
        responses={200: 'Withdraw successful'}
    )
    @extend_schema(tags=['operations'])
    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        account = self.get_object(pk)
        if account is None:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)


        serializer = DepositWithdrawSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            currency_code = serializer.validated_data.get('currency_code', 'NIS')
            try:
                account.withdraw(float(amount), currency_code)
                BankOperation.objects.create(account=account, operation_type='withdraw', amount=amount)
                return Response({"status": "Withdrawal successful"}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @extend_schema(tags=['operations'])
    @action(detail=True, methods=['get'])
    def balance(self, request, pk=None):
        account = self.get_object(pk)
        if account is None:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({"balance": account.balance}, status=status.HTTP_200_OK)



    @extend_schema(
        request=TransferSerializer,
        responses={200: 'Transfer successful'}
    )
    @extend_schema(tags=['operations'])
    @action(detail=False, methods=['post'])
    def transfer(self, request):
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            from_account_id = serializer.validated_data['from_account']
            to_account_id = serializer.validated_data['to_account']
            amount = serializer.validated_data['amount']
            currency_code = serializer.validated_data.get('currency_code', 'NIS')


            try:
                from_account = BankAccount.objects.get(pk=from_account_id)
                to_account = BankAccount.objects.get(pk=to_account_id)
            except BankAccount.DoesNotExist:
                return Response({'error': 'One or both accounts not found'}, status=status.HTTP_404_NOT_FOUND)


            try:
                from_account.transfer(amount, to_account, currency_code)
                BankOperation.objects.create(account=from_account, operation_type='transfer', amount=amount, recipient_account=to_account)
                return Response({"status": "Transfer successful"}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)