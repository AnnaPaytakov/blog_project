from django.urls import path
from .views import (
    BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView,
    FavoritesView, ToggleFavoriteView, ToggleLikeView
)

urlpatterns = [
    path('', BlogListView.as_view(), name='blogs'),
    path('blog/<str:pk>/', BlogDetailView.as_view(), name='blog'),

    path('add-blog/', BlogCreateView.as_view(), name='add-blog'),
    path('update-blog/<str:pk>/', BlogUpdateView.as_view(), name='update-blog'),
    path('delete-blog/<str:pk>/', BlogDeleteView.as_view(), name='delete-blog'),

    path('add_to_favorites/<str:pk>/', ToggleFavoriteView.as_view(), name='add_to_favorites'),
    path('user-favorites/', FavoritesView.as_view(), name='user-favorites'),

    path('toggle-like/', ToggleLikeView.as_view(), name='toggle_like'),
]