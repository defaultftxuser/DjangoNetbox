from django import forms
from .models import Device
from django.core.exceptions import ValidationError
from ipaddress import ip_address, AddressValueError


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'ip_address', 'address', "author", 'device_model', 'comment']

    def clean_ip_address(self):
        ip = self.cleaned_data['ip_address']
        try:
            ip_address(ip)
        except AddressValueError:
            raise ValidationError("Введите корректный IP-адрес.")
        return ip
