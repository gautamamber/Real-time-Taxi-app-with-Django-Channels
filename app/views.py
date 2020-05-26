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


class TripDetailApiView(generics.RetrieveAPIView):
    """
    Get trip details
    """
    lookup_field = 'id'
    lookup_url_kwarg = 'trip_id'
    permission_classes = (permissions.IsAuthenticated, )
    queryset = models.Trip.objects.all()
    serializer_class = serializers.TripSerializer


"""
users can participate in trips in one of two ways – they either drive the 
cars or they ride in them. A rider initiates the trip with a request, which 
is broadcast to all available drivers. A driver starts a trip by accepting the 
request. At this point, the driver heads to the pick-up address. The rider is instantly 
alerted that a driver has started the trip and other drivers are notified that the trip 
is no longer up for grabs.
"""
