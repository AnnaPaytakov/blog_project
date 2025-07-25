from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View, FormView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Post, Favorite, Category, Like
from .forms import BlogForm, CommentForm
from django.views.generic.edit import FormMixin
from django.urls import reverse
import requests
import os
from django.conf import settings

class BlogListView(ListView):
    model = Post
    template_name = 'blogs/blogs.html'
    context_object_name = 'all_blogs'
    paginate_by = 12

    def get_queryset(self):
        q_name = self.request.GET.get("q_name", "").strip()
        q_category = self.request.GET.get("q_category", "").strip()
        
        #if meilisearch exists and work
        if settings.USE_MEILISEARCH == "True" and (q_name or q_category):
            try:
                
                meili_host = os.getenv("MEILI_HOST", "http://127.0.0.1:7700")
                api_key = os.getenv("MEILISEARCH_API_KEY")
                headers = {"Content-Type": "application/json"}
                if api_key:
                    headers["Authorization"] = f"Bearer {api_key}"
                
                payload = {
                    "q": q_name,
                    "limit": 50,
                }
                
                filters = []
                if q_category:
                    filters.append(f'category = "{q_category}"')
                    
                if filters:
                    payload["filter"] = filters
                    
                response = requests.post(
                    f"{meili_host}/indexes/posts/search",
                    headers=headers,
                    json=payload,
                )
                results = response.json().get("hits", [])
                ids = [item["id"] for item in results]
                
                return Post.objects.filter(id__in=ids).order_by("-created_at")
            except Exception as e:
                print("Meilisearch error:", e)

        # if meilisearch doesnt work
        queryset = Post.objects.all().order_by('-created_at')
        if q_name:
            queryset = queryset.filter(
                translations__title__icontains=q_name
            ) | queryset.filter(
                translations__content__icontains=q_name
            )

        if q_category:
            queryset = queryset.filter(
                category__translations__name__icontains=q_category
            )
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all(),
            'current_language': 'en',
        })
        return context

class BlogDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'blogs/blog.html'
    context_object_name = 'blog'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.object
        context['comments'] = blog.comments.all()
        context['form'] = self.get_form()
        context['current_language'] = 'en'

        if self.request.user.is_authenticated:
            context['status'] = Favorite.objects.filter(user=self.request.user, blog=blog).exists()
            context['liked'] = Like.objects.filter(user=self.request.user, post=blog).exists()
        else:
            context['status'] = False
            context['liked'] = False

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = self.object
            comment.author = request.user.profile
            comment.save()
            return redirect(self.get_success_url())
        return self.form_invalid(form)

class BlogCreateView(LoginRequiredMixin, FormView):
    template_name = 'blogs/blog-form.html'
    form_class = BlogForm
    success_url = reverse_lazy('account')

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.author = self.request.user.profile
        blog.save()
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = BlogForm
    template_name = 'blogs/blog-form.html'
    success_url = reverse_lazy('account')


class BlogDeleteView(LoginRequiredMixin, View):
    template_name = 'blogs/delete-blog.html'
    success_url = reverse_lazy('account')

    def get(self, request, pk):
        blog = get_object_or_404(Post, id=pk)
        return render(request, self.template_name, {'blog': blog})

    def post(self, request, pk):
        blog = get_object_or_404(Post, id=pk)
        blog.delete()
        return redirect(self.success_url)


class FavoritesView(LoginRequiredMixin, TemplateView):
    template_name = 'blogs/favorites.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = Favorite.objects.filter(user=self.request.user)
        return context

class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        blog = get_object_or_404(Post, id=pk)
        favorite, created = Favorite.objects.get_or_create(user=request.user, blog=blog)
        if not created:
            favorite.delete()
            return JsonResponse({'added': False})
        return JsonResponse({'added': True})

class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request):
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        return JsonResponse({
            "liked": liked,
            "likes_count": Like.objects.filter(post=post).count()
        })