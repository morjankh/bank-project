from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet


app_name = 'user'
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)  # Register the CustomerViewSet

urlpatterns = [
    path('', include(router.urls)),  # Include all the router URLs
]



