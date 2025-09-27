import uuid
from django.db import models

class Transaction(models.Model):
    """
    Stores details of a single financial transaction.
    In real deployments, this is populated via webhooks (e.g. M-Pesa, bank APIs).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.CharField(max_length=50, help_text="Source of the transaction, e.g., mpesa, bank")
    provider_txn_id = models.CharField(max_length=100, unique=True, help_text="ID from provider")
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="KES")
    timestamp = models.DateTimeField(help_text="Timestamp from provider")
    processed = models.BooleanField(default=False, help_text="Has fraud detection been applied?")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.provider.upper()} {self.amount} {self.currency} from {self.sender}"
