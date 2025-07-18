from django.db import models
import uuid
from users.models import Profile
from django.contrib.auth.models import User
from django.utils.timezone import now
from parler.models import TranslatableModel, TranslatedFields

class Category(TranslatableModel):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    translations = TranslatedFields(name=models.CharField(max_length=100))
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Post(TranslatableModel):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    translations = TranslatedFields(
        title=models.CharField(max_length=500),
        content=models.TextField(null=True, blank=True),
    )
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    blog_image = models.ImageField(null=True, blank=True, default='default.jpg')
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)

    @property
    def likes_count(self):
        return self.likes.count()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
            
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        unique_together = ('user', 'post')

class Comment(models.Model):
    blog = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f'Comment by {self.author} on {self.blog}'

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='favorites', blank=True, null=True)
    blog = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return f'{self.user.username} - {self.blog.title}'

    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"