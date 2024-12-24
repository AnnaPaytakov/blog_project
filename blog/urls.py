from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('blog/<str:pk>/', views.blog, name='blog'),
    path('add-blog/', views.add_blog, name='add-blog'),
    path('update-blog/<str:pk>/', views.update_blog, name='update-blog'),
    path('delete-blog/<str:pk>/', views.delete_blog, name='delete-blog'),
    path('add_to_favorites/<str:pk>/', views.add_to_favorites, name='add_to_favorites'),
    path('user-favorites/', views.favorites_list, name='user-favorites'),
]