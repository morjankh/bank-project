from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from decimal import Decimal


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
    # OPERATION_CHOICES = [
    #     ('deposit', 'Deposit'),
    #     ('withdraw', 'Withdraw'),
    #     ('transfer', 'Transfer'),
    # ]

    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='operations')
    # operation_type = models.CharField(max_length=20, choices=OPERATION_CHOICES)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    recipient_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='incoming_transfers',
                                          blank=True, null=True)
    # timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.operation_type} - {self.amount} NIS on {self.account}"


class Currency(models.Model):
    code = models.CharField(max_length=3)  # e.g., 'USD', 'EUR'
    rate_to_nis = models.DecimalField(max_digits=10, decimal_places=4)  # Conversion rate to NIS
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.rate_to_nis} NIS"





