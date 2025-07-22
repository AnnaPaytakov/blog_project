from django.contrib import admin
from .models import Post, Favorite,Category,Comment,Like
from parler.admin import TranslatableAdmin

admin.site.register(Favorite)
admin.site.register(Comment)
admin.site.register(Like)

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('name', 'created')

@admin.register(Post)
class PostAdmin(TranslatableAdmin):
    list_display = ('title', 'author', 'created_at')