from rest_framework.routers import SimpleRouter

from src.presentation.api.devices.views import DeviceViewSet, DeviceModelViewSet

router = SimpleRouter()
router.register(r"devices", DeviceViewSet, basename="devices")
router.register(r"models", DeviceModelViewSet, basename="models")
