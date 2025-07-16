import os
import sys
import django
import json

# Настройка Django окружения
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

django.setup()

from django.core.serializers import serialize
from blog.models import Post, Comment, Like, Category, Favorite, TranslatedCategory # Расшири список, если появятся новые модели

models_to_dump = [Post, Comment, Like, Category, Favorite, TranslatedCategory]

# Собираем все данные
all_data = []
for model in models_to_dump:
    serialized = serialize('json', model.objects.all(), indent=2)
    all_data.extend(json.loads(serialized))  # сериализованные объекты — это список

# Сохраняем в файл с UTF-8
with open('blog_full_dump.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

print("✅ blog_full_dump.json успешно сохранён.")