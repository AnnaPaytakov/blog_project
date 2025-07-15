import os
import sys
import django
from django.conf import settings
import meilisearch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from blog.models import Post

INDEX_NAME = "posts"

def get_api_key():
    key_path = os.path.join(settings.BASE_DIR, 'meili_api_key.txt')
    try:
        with open(key_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        master_key = settings.DJANGO_MEILISEARCH["api_key"]
        client = meilisearch.Client(settings.DJANGO_MEILISEARCH["url"], master_key)
        try:
            key_info = client.create_key({
                "description": "Django API Key",
                "actions": ["*"],
                "indexes": ["*"],
                "expiresAt": None
            })
            api_key = key_info.key
            with open(key_path, 'w') as f:
                f.write(api_key)
            return api_key
        except Exception as e:
            print(f"Ошибка при создании API-ключа: {e}")
            return master_key

def update_meili_index():
    api_key = get_api_key()
    client = meilisearch.Client(settings.DJANGO_MEILISEARCH["url"], api_key)
    
    # Проверяем, существует ли индекс, и создаем, если нет
    try:
        client.get_index(INDEX_NAME)
    except:
        client.create_index(INDEX_NAME, {'primaryKey': 'id'})
    
    index = client.index(INDEX_NAME)
    posts = Post.objects.all()
    documents = [
        {
            "id": str(post.id),
            "title": post.title,
            "content": post.content,
            "author": post.author.user.username if post.author else "Unknown",
            "category": post.category.name if post.category else "No Category",
            "created_at": post.created_at.isoformat(),
        }
        for post in posts
    ]

    if documents:
        index.add_documents(documents)
        print(f"Загружено {len(documents)} документов в Meilisearch")
    else:
        print("Нет данных для загрузки")

if __name__ == "__main__":
    update_meili_index()