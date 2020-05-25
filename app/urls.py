from django.urls import path
from . import views


urlpatterns = [
    path('v1/signup', views.SignupApiView.as_view(), name="sign_up")
]
