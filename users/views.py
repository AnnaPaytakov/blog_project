from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Profile
from blog.models import Post
from .forms import CustomRegisterForm, AccountForm
from django.contrib.auth.decorators import login_required


def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    all_blogs = Post.objects.filter(author=profile)

    context = {
        'profile':profile,
        'all_blogs':all_blogs,
    }
    return render(request, 'users/profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    all_blogs = Post.objects.filter(author=profile)

    context = {
        'profile':profile,
        'all_blogs':all_blogs,
    }

    return render(request, 'users/account.html', context)

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('blogs')

    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'There is no such user')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('blogs')
        else:
            messages.error(request,'Wrong password')
    return render(request, 'users/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    form = CustomRegisterForm()

    if request.method=='POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('blogs')
    
    context = {
        'form':form,
    }
    return render(request, 'users/register.html', context)

def edit_account(request, pk):
    account = Profile.objects.get(id=pk)
    form = AccountForm(instance=account)

    if request.method=='POST':
        form = AccountForm(request.POST, request.FILES, instance=account)
        if form.is_valid():
            account = form.save(commit=False)

            if account.user.username != request.POST['username']:
                account.user.save()
                print('User changed username')

            account.save()
            return redirect('account')
        else:
            messages.error(request, 'Please, fill in the form correctly')

    context ={
        'form':form,
    }
    return render(request, 'users/account-form.html', context)