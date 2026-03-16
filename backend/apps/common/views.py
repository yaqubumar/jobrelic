from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(_request):
    return Response({"status": "ok", "service": "jobrelic-api"})


@api_view(["GET"])
def root_view(_request):
    return Response({
        "status": "ok",
        "service": "jobrelic-api",
        "message": "Welcome to Jobrelic. Visit /admin/ for admin panel or /api/ for API endpoints.",
    })
