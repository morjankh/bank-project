from django.urls import path
from .views import LoanViewSet

urlpatterns = [
    path('grant/', LoanViewSet.as_view({'post': 'grant_loan'}), name='grant-loan'),
    path('customer/', LoanViewSet.as_view({'get': 'customer_loans'}), name='customer-loans'),
    path('<int:pk>/repay/', LoanViewSet.as_view({'post': 'repay'}), name='repay-loan'),
]
