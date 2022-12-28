from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Post, Category, Subcategory, Comment
from .forms import CommentForm
from .utils import paginate

import random


def index_view(request):
    posts = Post.published_posts.all()
    paginator_context = paginate(request, posts)
    context = {
        **paginator_context
    }
    return render(request, 'blog/index_view.html', context)


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.published_posts.filter(subcategory__category__slug=slug)
    paginator_context = paginate(request, posts)
    context = {
        'category': category,
        **paginator_context
    }
    return render(request, 'blog/category_view.html', context)


def subcategory_view(request, slug):
    subcategory = get_object_or_404(Subcategory, slug=slug)
    posts = Post.published_posts.filter(subcategory__slug=slug)
    paginator_context = paginate(request, posts)
    context = {
        'subcategory': subcategory,
        **paginator_context
    }
    return render(request, 'blog/subcategory_view.html', context)


def post_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    ingredients = post.ingredients.all()
    photos = post.get_secondary_photos()
    similar_posts = Post.published_posts.filter(subcategory=post.subcategory).exclude(pk=post.pk)
    similar_posts_len = len(similar_posts) if len(similar_posts) <= 4 else 4
    similar_posts = random.sample(list(similar_posts), k=similar_posts_len)

    previous_post = Post.published_posts.filter(created_on__lt=post.created_on).first()
    next_post = Post.published_posts.filter(created_on__gt=post.created_on).last()

    comments = Comment.published_comments.filter(post=post, reply_to=None).order_by('-created_on')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = Comment(
                post=post,
                name=form.cleaned_data['name'],
                content=form.cleaned_data['content'],
                email=form.cleaned_data['email']
            )
            if request.user == post.created_by:
                new_comment.is_post_author = True
                new_comment.published = True
                new_comment.avatar = 'blog/author-user.png'
            try:
                reply_to_pk = int(form.cleaned_data['reply_to'])
                if reply_to_pk not in [comment.pk for comment in comments]:
                    new_comment.reply_to = None
                else:
                    reply_comment = Comment.objects.get(pk=reply_to_pk)
                    new_comment.reply_to = reply_comment
            except (TypeError, ValueError, Comment.DoesNotExist):
                new_comment.reply_to = None
            new_comment.save()
            messages.success(request, 'Twój komentarz został dodany i czeka na akceptację.')
            return redirect(post.get_absolute_url() + '#comment-add')
    else:
        form = CommentForm()
    captcha1 = random.randint(11, 29)
    captcha2 = random.randint(1, 9)
    valid_captcha = captcha1 - captcha2
    context = {
        'post': post,
        'ingredients': ingredients,
        'photos': photos,
        'similar_posts': similar_posts,
        'previous_post': previous_post,
        'next_post': next_post,
        'comments': comments,
        'form': form,
        'captcha1': captcha1,
        'captcha2': captcha2,
        'valid_captcha': valid_captcha
    }
    return render(request, 'blog/post_detail_view.html', context)


def newsletter_view(request):
    return render(request, 'blog/newsletter_view.html', {})
