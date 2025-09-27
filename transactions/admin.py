from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "provider", "provider_txn_id", "amount", "currency", "sender", "receiver", "timestamp", "processed")
    search_fields = ("provider_txn_id", "sender", "receiver")
    list_filter = ("provider", "currency", "processed")
