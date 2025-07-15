from django.contrib import admin
from .models import Post, Favorite, Category, Comment

admin.site.register(Post)
admin.site.register(Favorite)
admin.site.register(Category)
admin.site.register(Comment)