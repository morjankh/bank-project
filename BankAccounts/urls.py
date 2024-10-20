from rest_framework.routers import DefaultRouter
from .views import BankAccountViewSet

router = DefaultRouter()

router.register(r'accounts', BankAccountViewSet)  # Register the BankAccountViewSet

urlpatterns = router.urls
