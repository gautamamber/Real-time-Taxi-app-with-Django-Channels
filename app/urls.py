from django.urls import path
from . import views


urlpatterns = [
    path('', views.SignupApiView.as_view(), name="sign_up")
]
