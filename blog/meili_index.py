import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")
import django
django.setup()

from .models import Post, Category 
import requests

MEILI_HOST = "http://localhost:7700"
MEILI_API_KEY = os.getenv("MEILISEARCH_API_KEY", None)
HEADERS = {"Content-Type": "application/json"}
if MEILI_API_KEY:
    HEADERS["X-Meili-API-Key"] = MEILI_API_KEY

def index_posts():
    print("⏳ Indexing posts...")
    documents = [
        {
            "id": str(post.id),
            "title": post.title,
            "content": post.content,
            "author": str(post.author),
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
    index_posts()
    index_categories()