from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.adminsite, name='admin'),
]