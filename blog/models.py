from django.db import models
import uuid
from users.models import Profile
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(null=True, blank=True)
    blog_image = models.ImageField(null=True, blank=True, default='default.jpg')
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return self.title
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favortes')
    blog = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return f'{self.user.username} - {self.blog.title}'