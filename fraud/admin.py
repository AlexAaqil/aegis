from django.contrib import admin
from .models import FraudAlert

@admin.register(FraudAlert)
class FraudAlertAdmin(admin.ModelAdmin):
    list_display = ("id", "transaction", "rule", "severity", "resolved", "created_at")
    search_fields = ("transaction__provider_txn_id", "rule", "reason")
    list_filter = ("rule", "severity", "resolved")
