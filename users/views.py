from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView, FormView, UpdateView, View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Profile
from .forms import CustomRegisterForm, AccountForm
from blog.models import Post
from users.utils import send_mail_async
import os
from dotenv import load_dotenv

load_dotenv()

#* Profile we Blog ucin umumy Mixin
class ProfileContextMixin:
    def get_profile(self):
        raise NotImplementedError("Basga classlarda get_profile() berilmedik")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        context['profile'] = profile
        context['all_blogs'] = Post.objects.filter(author=profile)
        return context
    

class ProfileDetailView(ProfileContextMixin, DetailView):
    model = Profile
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_profile(self):
        return self.get_object()
    

class UserAccountView(LoginRequiredMixin, ProfileContextMixin, TemplateView):
    template_name = 'users/account.html'
    login_url = 'login'

    def get_profile(self):
        return self.request.user.profile
    

class LoginUserView(TemplateView):
    template_name = 'users/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blogs')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('blogs')
        messages.error(request, 'Adynyz yada parolynyz nadogry!')
        return self.get(request, *args, **kwargs)
    

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('blogs')


class RegisterUserView(FormView):
    template_name = 'users/register.html'
    form_class = CustomRegisterForm
    success_url = reverse_lazy('blogs')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        login(self.request, user)
        
        send_mail_async(
            subject='Welcome to our News Blog!',
            message='Thank you for your registration! Enjoy your time!',
            from_email=os.environ.get('EMAIL_HOST_USER'),
            recipient_list=[user.email],
            fail_silently=True
        )

        return super().form_valid(form)
    
    
class EditAccountView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = AccountForm
    template_name = 'users/account-form.html'
    success_url = reverse_lazy('account')
    login_url = 'login'

    def form_valid(self, form):
        account = form.save(commit=False)
        if account.user.username != self.request.POST.get('username'):
            account.user.save()
        account.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Maglumatlary dogry dolduruň!')
        return super().form_invalid(form)
    

class ForgotPasswordView(TemplateView):
    template_name = 'users/forgot-password.html'
    