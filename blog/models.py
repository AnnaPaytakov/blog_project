from django.db import models
import uuid
from users.models import Profile
from django.contrib.auth.models import User
from django.utils.timezone import now

from parler.models import TranslatableModel, TranslatedFields


class TranslatedCategory(TranslatableModel):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    translations = TranslatedFields(name=models.CharField(max_length=100))

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_ru = models.CharField(max_length=100, unique=True, blank=True, null=True)
    name_tm = models.CharField(max_length=100, unique=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=500)
    title_ru = models.CharField(max_length=500, blank=True, null=True)
    title_tm = models.CharField(max_length=500, blank=True, null=True)
    content = models.TextField(null=True, blank=True)
    content_ru = models.TextField(null=True, blank=True)
    content_tm = models.TextField(null=True, blank=True)
    blog_image = models.ImageField(null=True, blank=True, default='default.jpg')
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    class MeiliSearch:
        index_name = "posts"
        attributes_to_index = ["title", "content", "title_ru", "content_ru", "title_tm", "content_tm"]
        attributes_to_retrieve = ["title", "content", "created_at"]
        searchable_attributes = ["title", "content", "title_ru", "content_ru", "title_tm", "content_tm"]

    def __str__(self):
        return self.title
    
    @property
    def likes_count(self):
        return self.likes.count()
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class Comment(models.Model):
    blog = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f'Comment by {self.author} on {self.blog}'

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favortes')
    blog = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return f'{self.user.username} - {self.blog.title}'