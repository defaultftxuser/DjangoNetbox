from abc import ABC
from dataclasses import dataclass

from django.db import IntegrityError

from src.infra.exceptions.repo_exceptions import UserAlreadyExistsException
from src.infra.repos.base import GenericRepository
from src.infra.repos.devices.devices_repos import DeviceRepository, DeviceModelRepository
from src.infra.repos.users.users_repo import UserRepository, TokenRepository


@dataclass(eq=False)
class BaseDeviceService(ABC):
    repository: GenericRepository


@dataclass(eq=False)
class DeviceService(BaseDeviceService):
    repository: DeviceRepository


@dataclass(eq=False)
class DeviceModelService(BaseDeviceService):
    repository: DeviceModelRepository
