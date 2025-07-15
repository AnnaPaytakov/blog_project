from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('ru/', views.blogs_ru, name='blogs_ru'),
    path('tm/', views.blogs_tm, name='blogs_tm'),
    path('blog/<str:pk>/', views.blog, name='blog'),
    path('blog/ru/<str:pk>/', views.blog_ru, name='blog_ru'),
    path('blog/tm/<str:pk>/', views.blog_tm, name='blog_tm'),
    path('add-blog/', views.add_blog, name='add-blog'),
    path('update-blog/<str:pk>/', views.update_blog, name='update-blog'),
    path('delete-blog/<str:pk>/', views.delete_blog, name='delete-blog'),
    path('add_to_favorites/<str:pk>/', views.add_to_favorites, name='add_to_favorites'),
    path('user-favorites/', views.favorites_list, name='user-favorites'),
    path('user-favorites-ru/', views.favorites_list_ru, name='user-favorites-ru'),
    path('user-favorites-tm/', views.favorites_list_tm, name='user-favorites-tm'),
    path('toggle-like/', views.toggle_like, name='toggle_like'),
    path('search/', views.search_posts, name='search_posts'),
]