from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    ProfileDetailView, UserAccountView, LoginUserView, LogoutView,
    RegisterUserView, EditAccountView, ForgotPasswordView
)

urlpatterns = [
    path('profile/<str:pk>/', ProfileDetailView.as_view(), name='profile'),

    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),

    path('account/', UserAccountView.as_view(), name='account'),
    path('edit-account/<str:pk>/', EditAccountView.as_view(), name='edit-account'),

    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]