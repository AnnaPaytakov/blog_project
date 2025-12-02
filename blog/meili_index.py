import os
import sys
import requests
from blog.models import Post, Category
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")
django.setup()


MEILI_HOST = "http://localhost:7700"
MEILI_API_KEY = os.getenv("MEILISEARCH_API_KEY", None)
HEADERS = {"Content-Type": "application/json"}
if MEILI_API_KEY:
    HEADERS["Authorization"] = f"Bearer {MEILI_API_KEY}"

def configure_posts_index():
    print("⚙️ Configuring filterable attributes for posts...")
    res = requests.put(
        f"{MEILI_HOST}/indexes/posts/settings/filterable-attributes",
        headers=HEADERS,
        json=["category"]
    )
    print(f"✅ Filterable set: {res.status_code} | {res.text}")

def index_posts():
    print("⏳ Indexing posts...")
    documents = [
        {
            "id": str(post.id),
            "title": post.title,
            "content": post.content,
            "author": str(post.author) if post.author else None,
            "category": post.category.name if post.category else None,
        }
        for post in Post.objects.all()
    ]
    res = requests.put(f"{MEILI_HOST}/indexes/posts/documents", json=documents, headers=HEADERS)
    print(f"✅ Posts indexed: {res.status_code}\nResponse text: {res.text}")

def index_categories():
    print("⏳ Indexing categories...")
    documents = [
        {
            "id": str(category.id),
            "name": category.name,
        }
        for category in Category.objects.all()
    ]
    res = requests.put(f"{MEILI_HOST}/indexes/categories/documents", json=documents, headers=HEADERS)
    print(f"✅ Categories indexed: {res.status_code}\nResponse text: {res.text}")

if __name__ == "__main__":
    configure_posts_index()
    index_posts()
    index_categories()