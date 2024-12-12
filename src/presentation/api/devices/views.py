from django.http import JsonResponse

from dadata import Dadata
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from src.infra.permissions.permissions import IsAdminOrReadOnly
from src.infra.serializers.devices.serializers import DeviceSerializer, DeviceModelSerializer
from src.infra.settings.settings import get_env
from src.presentation.apps.device_app.models import Device, DeviceModel


def dadata_suggest(request):
    query = request.GET.get("query", "")
    if not query:
        return JsonResponse({"error": "Query parameter is required"}, status=400)

    token = get_env()("DADATA_API_KEY")
    dadata = Dadata(token)
    suggestions = dadata.suggest("address", query)
    return JsonResponse({"suggestions": suggestions})


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Только авторизованные пользователи могут добавлять устройства.")
        serializer.save(author=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return Device.objects.all()
        elif self.request.user.is_authenticated:
            return Device.objects.filter(author=self.request.user)


class DeviceModelViewSet(ModelViewSet):
    queryset = DeviceModel.objects.all()
    serializer_class = DeviceModelSerializer
    permission_classes = [IsAdminOrReadOnly]
