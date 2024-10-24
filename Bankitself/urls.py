from django.urls import path
from .views import BankViewSet

urlpatterns = [
    path('balance/', BankViewSet.as_view({'get': 'retrieve_balance'}), name='bank-balance'),
]