from dataclasses import dataclass

from django.db.models import QuerySet

from src.infra.repos.base import GenericRepository
from src.presentation.apps.device_app.models import Device, DeviceModel


@dataclass(eq=False)
class DeviceRepository(GenericRepository):
    model: Device = Device
    queryset: QuerySet = Device.objects.all()


@dataclass(eq=False)
class DeviceModelRepository(GenericRepository):
    model: DeviceModel = DeviceModel
    queryset: QuerySet = DeviceModel.objects.all()
