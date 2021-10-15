from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model

from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    """
    Register
    To start using the API - you must first create a user.
    """
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer
