from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    BlockUserView,
    ChangePasswordView,
    PasswordResetView,
    RegisterView,
    UserDetailView,
    UserListView,
    email_verification, LoginCustomsView, UserUpdateView,
)

app_name = "user"


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginCustomsView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="reservation:home"), name="logout"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("user_list/", UserListView.as_view(), name="user_list"),
    path("user_block/<int:user_id>", BlockUserView.as_view(), name="user_block"),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("profile/<int:pk>", UserDetailView.as_view(), name="user_profile"),
    path("user_update/<int:pk>/", UserUpdateView.as_view(), name="user_update")
]