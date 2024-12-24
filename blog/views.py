from django.shortcuts import render, redirect
from .models import Post, Favorite
from .forms import BlogForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

def blogs(request):
    q_name = request.GET.get('q_name')
    all_blogs= Post.objects.all()

    if q_name:
        all_blogs = all_blogs.filter(title__icontains=q_name)
    
    context = {
        'all_blogs': all_blogs,
    }
    return render(request, 'blogs/blogs.html', context)

def blog(request, pk):
    blog = Post.objects.get(id=pk)
    status = False
    if request.user.is_authenticated:
        status = Favorite.objects.filter(user=request.user, blog=blog).exists()
    context = {
        'blog':blog,
        'status':status,
        }
    return render(request, 'blogs/blog.html', context)

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