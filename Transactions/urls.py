from django.urls import path
from .views import TransactionViewSet

urlpatterns = [
    path('transactions/', TransactionViewSet.as_view({'get': 'list'}), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionViewSet.as_view({'get': 'retrieve'}), name='transaction-detail'),
]