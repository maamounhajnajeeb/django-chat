from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


app_name = "api"

urlpatterns = [
    path("log_in/", TokenObtainPairView.as_view(), name="log-in"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("sign_up/", views.SignUpView.as_view(), name="sign-up"),
    path("activate_user/<int:user_id>/", views.activate_account, name="activate_account"),
]
