from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import FraudAlert
from .serializers import FraudAlertSerializer
from django.db import transaction


class FraudAlertViewSet(viewsets.ModelViewSet):
    queryset = FraudAlert.objects.all().order_by("-created_at")
    serializer_class = FraudAlertSerializer

    @action(detail=True, methods=["patch"], url_path="resolve")
    def resolve_alert(self, request, pk=None):
        """Custom endpoint: PATCH /api/v1/alerts/{id}/resolve/"""
        alert = self.get_object()
        if alert.resolved:
            return Response({"detail": "Alert already resolved."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure DB transaction commits the update
        with transaction.atomic():
            alert.resolved = True
            alert.save(update_fields=["resolved"])  # only update resolved field

        alert.refresh_from_db()  # reload from DB to confirm
        return Response(FraudAlertSerializer(alert).data, status=status.HTTP_200_OK)