from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.profiles.api import _get_or_create_demo_profile

from .services import get_dashboard


@api_view(["GET"])
def dashboard(_request):
    profile = _get_or_create_demo_profile()
    return Response(get_dashboard(profile))
