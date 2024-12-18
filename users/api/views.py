"""
Importações do Django REST framework e dos Users
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from users.api.serializers import UserProfileExampleSerializer

from users.models import UserProfileExample


class UserProfileExampleViewSet(ModelViewSet):
    """
    ViewSet para gerenciamento de Users
    """
    serializer_class = UserProfileExampleSerializer
    permission_classes = [AllowAny]
    queryset = UserProfileExample.objects.all()
