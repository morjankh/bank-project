from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta


################################################################################################
class Customer(AbstractUser):
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

################################################################################################
class BankAccount(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='caccounts')
    account_type = models.CharField(max_length=20, choices=[('savings', 'Savings'), ('checking', 'Checking')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(default=False)  # Indicates if the account is closed
    has_loan = models.BooleanField(default=False)  # Indicates if the account has a loan

    def __str__(self):
        return f"Account {self.account_number} - {self.customer.username}"

    def close(self):
        """Close the account if there is no outstanding loan or negative balance."""
        if self.has_loan:
            raise ValueError("Account cannot be closed due to an outstanding loan")
        if self.balance < 0:
            raise ValueError("Account cannot be closed with a negative balance")
        self.closed = True
        self.save()

    def deposit(self, amount, currency_code):
        if currency_code == 'NIS':
         if amount <= 0:
              raise ValueError("Deposit amount must be positive.")
         self.balance += Decimal(amount)
         self.save()
        else:
            try:
                currency = Currency.objects.get(code=currency_code)
                amount_in_nis = Decimal(amount) * currency.rate_to_nis  # Convert foreign amount to NIS
                self.balance += amount_in_nis
                self.save()
            except Currency.DoesNotExist:
                raise ValueError(f"Currency {currency_code} not supported.")

        self.save()  # Save the updated account balance

        # Adjust the bank balance
        bank = Bank.objects.first()  # Assuming there's only one bank instance
        if bank is None:
            raise ValueError("Bank not found.")  # Ensure the bank instance exists

        # Increase bank balance by the deposit amount
        if currency_code == 'NIS':
            bank.adjust_balance(Decimal(amount))  # Increase bank balance for NIS deposit
        else:
            bank.adjust_balance(amount_in_nis)  # Increase bank balance for foreign currency deposit

        bank.save()  # Save the updated bank balance

    def withdraw(self, amount, currency_code):
       if currency_code == 'NIS':
         if Decimal(amount) > self.balance:
            raise ValueError("Insufficient funds for withdrawal.")
         self.balance -= Decimal(amount)
         self.save()
       else:
        try:
            currency = Currency.objects.get(code=currency_code)
            amount_in_nis = Decimal(amount) * currency.rate_to_nis
            if amount_in_nis > self.balance:
                raise ValueError("Insufficient funds for withdrawal.")
            self.balance -= amount_in_nis
            self.save()
        except Currency.DoesNotExist:
            raise ValueError(f"Currency {currency_code} not supported.")


    def transfer(self, amount, recipient_account, currency_code='NIS'):
        """
        Transfer money from this account to the recipient account.
        """
        if currency_code == 'NIS':
            # Transfer in NIS without conversion
            if Decimal(amount) > self.balance:
                raise ValueError("Insufficient funds for transfer.")
            self.balance -= Decimal(amount)
            recipient_account.balance += Decimal(amount)
            self.save()
            recipient_account.save()
        else:
            try:
                currency = Currency.objects.get(code=currency_code)
                amount_in_nis = Decimal(amount) * currency.rate_to_nis

                if amount_in_nis > self.balance:
                    raise ValueError("Insufficient funds for transfer.")

                self.balance -= amount_in_nis
                self.save()
                recipient_account.balance += amount_in_nis
                recipient_account.save()

            except Currency.DoesNotExist:
                raise ValueError(f"Currency {currency_code} not supported.")

################################################################################################
class BankOperation(models.Model):
    OPERATION_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('transfer', 'Transfer'),
    ]

    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='operations')
    operation_type= models.CharField(max_length=20, choices=OPERATION_CHOICES)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    recipient_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='incoming_transfers',
                                          blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # Remove the 'default' here

    def __str__(self):
        return f"{self.operation_type} - {self.amount} NIS on {self.account}"


class Currency(models.Model):
    code = models.CharField(max_length=3)  # e.g., 'USD', 'EUR'
    rate_to_nis = models.DecimalField(max_digits=10, decimal_places=4)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.rate_to_nis} NIS"
################################################################################################
class Loans(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='loans')
    account = models.ForeignKey('BankAccount', on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)
    granted_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    paid_off = models.BooleanField(default=False)
    months = models.IntegerField(default=12)

    def grant_loan(self):
        """ Initializes the loan and sets the due date. """
        self.remaining_balance = self.amount
        self.due_date = timezone.now().date() + timedelta(days=365)


        bank_account = self.account
        bank_account.balance += self.amount
        bank_account.has_loan = True
        bank_account.save()

        self.save()

    def repay(self, repayment_amount):
        """ Repays part of the loan based on the fixed monthly amount. """
        monthly_repayment = (self.amount * self.interest_rate) / 100

        if repayment_amount != monthly_repayment:
            raise ValueError(f"Expected repayment is {monthly_repayment}, but received {repayment_amount}.")

        self.remaining_balance -= repayment_amount
        self.months -= 1
        bank_account = self.account
        bank_account.balance -= repayment_amount
        bank_account.save()
        if self.remaining_balance <= 0 or self.months <= 0:
            self.remaining_balance = 0
            self.paid_off = True
            bank_account.has_loan = False
            bank_account.save()

        self.save()
################################################################################################
class Bank(models.Model):
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=10000000.00)  # Start with 1,000,000 NIS

    def __str__(self):
            return f"Bank Balance: {self.balance} NIS"

    def adjust_balance(self, amount):
        """
        Adjust the bank balance by the given amount (can be positive or negative).
        """
        self.balance += amount
        self.save()