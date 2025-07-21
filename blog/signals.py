from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Post, Category

@receiver(pre_save, sender=Post)
def generate_slug_for_post(sender, instance, **kwargs):
    if not instance.slug:
        title = instance.safe_translation_getter('title', any_language=True)
        instance.slug = slugify(title)

@receiver(pre_save, sender=Category)
def generate_slug_for_category(sender, instance, **kwargs):
    if not instance.slug:
        name = instance.safe_translation_getter('name', any_language=True)
        instance.slug = slugify(name)