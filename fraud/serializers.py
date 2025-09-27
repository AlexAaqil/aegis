from rest_framework import serializers
from .models import FraudAlert

class FraudAlertSerializer(serializers.ModelSerializer):
    transaction = serializers.StringRelatedField()  # shows transaction summary

    class Meta:
        model = FraudAlert
        fields = "__all__"
