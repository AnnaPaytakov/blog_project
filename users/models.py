from django.db import models
from django.contrib.auth.models import User
import uuid
from django_resized import ResizedImageField
from django.core.mail import send_mail
from django.utils.timezone import now
from django.urls import reverse
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    profile_image = ResizedImageField(blank=True, null=True, default='profiles/user-default.png', upload_to='profiles/',)
    firstname = models.CharField(max_length=50,blank=True, null=True)
    lastname = models.CharField(max_length=50,blank=True, null=True)
    username = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    def __str__(self):
        return str(self.username)