from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets
from . import serializers, models
from rest_framework_simplejwt.views import TokenObtainPairView


class SignupApiView(generics.CreateAPIView):
    """
    Sign up api view
    """
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer


class LoginApiView(TokenObtainPairView):
    """
    Login api view with jwt token
    """
    serializer_class = serializers.LoginSerializer


class TripApiView(generics.ListAPIView):
    """
    Trip api view
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Trip.objects.all()
    serializer_class = serializers.TripSerializer
