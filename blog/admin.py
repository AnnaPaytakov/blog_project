from django.contrib import admin
from .models import Post, Favorite

admin.site.register(Post)
admin.site.register(Favorite)