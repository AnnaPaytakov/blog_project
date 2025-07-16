from django.contrib import admin
from .models import Post, Favorite, Category, Comment, TranslatedCategory
from parler.admin import TranslatableAdmin

admin.site.register(Post)
admin.site.register(Favorite)
admin.site.register(Category)
admin.site.register(Comment)
@admin.register(TranslatedCategory)
class TranslatedCategoryAdmin(TranslatableAdmin):
    list_display = ('__str__',)