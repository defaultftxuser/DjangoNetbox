from rest_framework import serializers

from src.presentation.apps.device_app.models import Device, DeviceModel


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["address", "name", "ip_address", "device_model"]


class DeviceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceModel
        fields = ["name", "description"]
