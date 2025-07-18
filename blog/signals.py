# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# import meilisearch
# from django.conf import settings
# from .models import Post

# INDEX_NAME = "posts"

# # Инициализация клиента MeiliSearch из настроек
# client = meilisearch.Client(settings.DJANGO_MEILISEARCH["url"])

# @receiver(post_save, sender=Post)
# def index_post(sender, instance, **kwargs):
#     index = client.index(INDEX_NAME)
#     document = {
#         "id": str(instance.id),
#         "title": instance.title,
#         "content": instance.content,
#         "author": instance.author.user.username if instance.author else "Unknown",
#         "category": instance.category.name if instance.category else "No Category",
#         "created_at": instance.created_at.isoformat(),
#     }
#     index.add_documents([document])

# @receiver(post_delete, sender=Post)
# def delete_post(sender, instance, **kwargs):
#     index = client.index(INDEX_NAME)
#     index.delete_document(str(instance.id))

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