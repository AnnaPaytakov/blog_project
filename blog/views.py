from django.shortcuts import render, redirect
from .models import Post, Favorite, Comment, Category, Like
from .forms import BlogForm
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
import meilisearch
from django.conf import settings
import os

# Используем мастер-ключ напрямую
master_key = os.environ.get("MEILI_MASTER_KEY", "supersecretkey123")
meilisearch_client = meilisearch.Client(settings.DJANGO_MEILISEARCH["url"], master_key)
meilisearch_index = meilisearch_client.index("posts")

def search_posts(request):
    query = request.GET.get("q", "").strip()
    results = {"hits": []}
    if query:
        try:
            results = meilisearch_index.search(query)
        except Exception as e:
            print(f"Meilisearch error: {e}")

    return render(request, "blog/search.html", {"results": results["hits"], "query": query})


def blogs(request):
    q_name = request.GET.get("q_name", "").strip()
    q_category = request.GET.get("q_category", "").strip()
    page_number = request.GET.get("page")

    if q_name:
        try:
            results = meilisearch_index.search(q_name)
            post_ids = [hit["id"] for hit in results["hits"]]
            all_blogs = Post.objects.filter(id__in=post_ids)
        except Exception as e:
            print(f"Meilisearch error: {e}")
            all_blogs = Post.objects.none()
    else:
        all_blogs = Post.objects.all().order_by('created_at')

    if q_category:
        all_blogs = all_blogs.filter(category__name=q_category)

    categories = Category.objects.all()
    paginator = Paginator(all_blogs, 12)
    page_obj = paginator.get_page(page_number)

    context = {
        "all_blogs": page_obj,
        "categories": categories,
        "page_obj": page_obj,
        "cookies_accepted": request.COOKIES.get("cookies_accepted"),
        "current_language": "en",
    }
    return render(request, "blogs/blogs.html", context)


def blogs_ru(request):
    q_name = request.GET.get('q_name')
    q_category = request.GET.get('q_category')
    all_blogs = Post.objects.all().order_by('-created_at')
    page_number = request.GET.get('page')

    if q_name:
        all_blogs = all_blogs.filter(
            Q(title_ru__icontains=q_name) | 
            Q(content_ru__icontains=q_name)
        )

    if q_category:
        all_blogs = all_blogs.filter(category__name_ru=q_category)
    
    categories = Category.objects.all()
    paginator = Paginator(all_blogs, 12)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'all_blogs': page_obj,
        'categories': categories,
        'page_obj': page_obj,
        'current_language':'ru',
    }
    return render(request, 'blogs/blogs_ru.html', context)

def blogs_tm(request):
    q_name = request.GET.get('q_name')
    q_category = request.GET.get('q_category')
    all_blogs = Post.objects.all().order_by('-created_at')
    page_number = request.GET.get('page')

    if q_name:
        all_blogs = all_blogs.filter(
            Q(title_tm__icontains=q_name) | 
            Q(content_tm__icontains=q_name)
        )

    if q_category:
        all_blogs = all_blogs.filter(category__name_tm=q_category)
    
    categories = Category.objects.all()
    paginator = Paginator(all_blogs, 12)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'all_blogs': page_obj,
        'categories': categories,
        'page_obj': page_obj,
        'current_language':'tm',
    }
    return render(request, 'blogs/blogs_tm.html', context)


def blog(request, pk):
    blog = Post.objects.get(id=pk) 
    comments = blog.comments.all()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user.profile
            comment.save()
            return redirect('blog', pk=blog.pk)
    else:
        form = CommentForm()

    status = False
    liked =False
    if request.user.is_authenticated:
        status = Favorite.objects.filter(user=request.user, blog=blog).exists()
        liked = Like.objects.filter(user=request.user).exists()
    context = {
        'blog':blog,
        'status':status,
        'liked':liked,
        'comments': comments,
        'form':form,
        'current_language': 'en',
        }
    return render(request, 'blogs/blog.html', context)

def blog_ru(request, pk):
    blog = Post.objects.get(id=pk)
    comments = blog.comments.all()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user.profile
            comment.save()
            return redirect('blog_ru', pk=blog.pk)
    else:
        form = CommentForm()

    status = False
    if request.user.is_authenticated:
        status = Favorite.objects.filter(user=request.user, blog=blog).exists()

    context = {
        'blog': blog,
        'status': status,
        'comments': comments,
        'form': form,
        'current_language':'ru',
    }
    return render(request, 'blogs/blog_ru.html', context)

def blog_tm(request, pk):
    blog = Post.objects.get(id=pk)
    comments = blog.comments.all()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user.profile
            comment.save()
            return redirect('blog_tm', pk=blog.pk)
    else:
        form = CommentForm()

    status = False
    if request.user.is_authenticated:
        status = Favorite.objects.filter(user=request.user, blog=blog).exists()

    context = {
        'blog': blog,
        'status': status,
        'comments': comments,
        'form': form,
        'current_language':'tm',
    }
    return render(request, 'blogs/blog_tm.html', context)

@login_required
def toggle_like(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)
        user = request.user

        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return JsonResponse({
            "liked": liked,
            "likes_count": Like.objects.filter(post=post).count()
        })
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def add_to_favorites(request, pk):
    blog = Post.objects.get(id=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, blog=blog)

    if not created:
        favorite.delete()
        return JsonResponse({'added':False})
    return JsonResponse({'added':True})

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    context = {
        'favorites':favorites,
    }
    return render(request, 'blogs/favorites.html', context)

@login_required
def favorites_list_ru(request):
    favorites = Favorite.objects.filter(user=request.user)
    context = {
        'favorites':favorites,
    }
    return render(request, 'blogs/favorites_ru.html', context)

@login_required
def favorites_list_tm(request):
    favorites = Favorite.objects.filter(user=request.user)
    context = {
        'favorites':favorites,
    }
    return render(request, 'blogs/favorites_tm.html', context)


@login_required(login_url='login')
def add_blog(request):
    form = BlogForm()
    if request.method == 'POST':
        form=BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user.profile
            form.save()
            return redirect('account')
        else:
            messages.error(request, 'Fill the form correctly')

    context = {
        'form':form,
    }
    return render(request, 'blogs/blog-form.html', context)

@login_required(login_url='login')
def update_blog(request, pk):
    blog = Post.objects.get(id=pk)
    form = BlogForm(instance=blog)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('account')
        
    context = {
        'form':form,
    }
    return render(request, 'blogs/blog-form.html', context)

@login_required(login_url='login')
def delete_blog(request, pk):
    blog = Post.objects.get(id=pk)

    if request.method == "POST":
        blog.delete()
        return redirect('account')
    
    context = {
        'blog':blog,
    }
    return render(request, 'blogs/delete-blog.html', context)