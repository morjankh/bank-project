from django.urls import path
from .views import BankOperationViewSet

urlpatterns = [
    path('deposit/<int:pk>/', BankOperationViewSet.as_view({'post': 'deposit'}), name='deposit'),
    path('withdraw/<int:pk>/', BankOperationViewSet.as_view({'post': 'withdraw'}), name='withdraw'),
    path('balance/<int:pk>/', BankOperationViewSet.as_view({'get': 'balance'}), name='balance'),
    path('transfer/', BankOperationViewSet.as_view({'post': 'transfer'}), name='transfer'),
]
