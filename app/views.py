from django.contrib.auth import get_user_model
from rest_framework import generics
from . import serializers


class SignupApiView(generics.CreateAPIView):
    """
    Sign up api view
    """
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
