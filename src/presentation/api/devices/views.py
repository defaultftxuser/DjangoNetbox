from django.http import JsonResponse

from dadata import Dadata
from src.infra.settings.settings import get_env


def dadata_suggest(request):
    query = request.GET.get("query", "")
    if not query:
        return JsonResponse({"error": "Query parameter is required"}, status=400)

    token = get_env()("DADATA_API_KEY")
    dadata = Dadata(token)
    suggestions = dadata.suggest("address", query)
    return JsonResponse({"suggestions": suggestions})
