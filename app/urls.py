from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('v1/signup', views.SignupApiView.as_view(), name="sign_up"),
    path('v1/login', views.LoginApiView.as_view(), name="login"),
    path('v1/token/refresh', TokenRefreshView.as_view(), name="token_refresh")
]
