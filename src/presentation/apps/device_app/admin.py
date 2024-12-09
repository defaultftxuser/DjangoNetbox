from django.contrib import admin

from src.presentation.apps.device_app.forms import DeviceForm
from src.presentation.apps.device_app.models import DeviceModel, Device


@admin.register(DeviceModel)
class DeviceModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    form = DeviceForm
    list_display = ('name', 'ip_address', 'author', 'device_model', 'address')
    list_filter = ('device_model', 'author')
    search_fields = ('name', 'ip_address', 'address')

    class Media:
        js = ('dadata_autocomplete.js',)
