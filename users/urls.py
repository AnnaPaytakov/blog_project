from django.urls import path
from .import views

urlpatterns = [
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('account/', views.userAccount, name='account'),
    path('edit-account/<str:pk>/', views.edit_account, name='edit-account'),
]