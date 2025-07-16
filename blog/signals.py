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