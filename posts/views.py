from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.db.models import Prefetch
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Post created.')
            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


def post_list(request):
    
    posts_qs = Post.objects.select_related('author').prefetch_related('likes', 'comments') 
    paginator = Paginator(posts_qs, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'post_list.html', {'page_obj': page_obj})


def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related('author').prefetch_related('comments__author', 'likes'), pk=pk)
    comment_form = CommentForm()
    is_liked = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(pk=request.user.pk).exists()
    return render(request, 'post_detail.html', {
        'post': post,
        'comment_form': comment_form,
        'is_liked': is_liked,
    })


@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'likes_count': post.likes_count()})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('posts:post_detail', args=[pk])))


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': comment.pk,
                    'author': comment.author.username,
                    'text': comment.text,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'comments_count': post.comments_count()
                })
    return redirect('posts:post_detail', pk=pk)



@login_required
def delete_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, post_id=post_pk)
    if comment.author != request.user and comment.post.author != request.user:
        messages.error(request, "You don't have permission to delete this comment.")
        return redirect('posts:post_detail', pk=post_pk)
    comment.delete()
    messages.success(request, 'Comment deleted.')
    return redirect('posts:post_detail', pk=post_pk)

