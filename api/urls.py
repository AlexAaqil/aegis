from django.urls import path, include
from rest_framework.routers import DefaultRouter
from transactions.views import TransactionViewSet
from fraud.views import FraudAlertViewSet

router = DefaultRouter()
router.register(r"transactions", TransactionViewSet)
router.register(r"alerts", FraudAlertViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
]
