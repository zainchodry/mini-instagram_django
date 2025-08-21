from django.shortcuts import render, redirect, get_object_or_404
from . models import *
from . forms import *
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from posts.models import Post





def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Accout Were Created Successfully")
            return redirect("accounts:login")
    form = RegisterForm()
    return render(request, "register.html", {"form":form})




def logout(request):
    auth_logout(request)
    messages.success(request, "You Logout Successfully")
    return redirect("accounts:login")



@login_required
def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile

    
    is_following = False
    if request.user.is_authenticated:
        is_following = profile.followers.filter(id=request.user.profile.id).exists()

    
    posts = Post.objects.filter(author=user).order_by('-created_at')

    return render(request, 'profile_detail.html', {
        'profile': profile,
        'is_following': is_following,
        'posts': posts
    })



@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect(reverse('accounts:profile_detail', args=[request.user.username]))
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile = target_user.profile
    profile = request.user.profile
    if target_profile == profile:
        messages.error(request, "You can't follow yourself")
        return redirect('accounts:profile_detail', username=username)
    if profile.following.filter(id=target_profile.id).exists():
        profile.following.remove(target_profile)
    else:
        profile.following.add(target_profile)
    return redirect('accounts:profile_detail', username=username)





def user_search(request):
    q = request.GET.get('q', '')
    results = []
    if q:
        results = User.objects.filter(Q(username__icontains=q) | Q(email__icontains=q))
    return render(request, 'user_list.html', {'results': results, 'q': q})







def index(request):
    if request.user.is_authenticated:
        
        users = User.objects.exclude(id=request.user.id)[:36]
    else:
        users = User.objects.all()[:36]
    return render(request, 'index.html', {'users': users})


