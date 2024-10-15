from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.
class Customer(AbstractUser):
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username


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

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
       if  amount <= self.balance :
              self.balance -= amount
              self.save()
       else:
           raise ValueError('Amount must be greater than or equal to balance')


    def close(self):
        """Close the account if there is no outstanding loan or negative balance."""
        if self.has_loan:
            raise ValueError("Account cannot be closed due to an outstanding loan")
        if self.balance < 0:
            raise ValueError("Account cannot be closed with a negative balance")
        self.closed = True
        self.save()
