from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator
from django.http import Http404
from django.core.mail import send_mail

from blog.models import Post, Ingredient, Photo, Category, Subcategory, NewsletterSubscriber, Comment
from blog.forms import CommentForm
import re
import random


def index_view(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(published=True)
    paginator = Paginator(posts, 4)
    page_nr = request.GET.get('page', 1)
    try:
        page_nr = int(page_nr)
        if page_nr < 1:
            page_nr = 1
        elif page_nr > paginator.num_pages:
            page_nr = paginator.num_pages
    except ValueError:
        page_nr = 1
    page_obj = paginator.get_page(page_nr)
    page_range = paginator.get_elided_page_range(page_nr, on_each_side=2, on_ends=1)
    context = {
        'categories': categories,
        'page_obj': page_obj,
        'page_range': page_range
    }
    return render(request, 'blog/index_view.html', context)


def category_view(request, slug):
    categories = Category.objects.all()
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        category = None
    posts = Post.objects.filter(published=True, subcategory__category__slug__exact=slug)
    paginator = Paginator(posts, 4)
    page_nr = request.GET.get('page', 1)
    try:
        page_nr = int(page_nr)
        if page_nr < 1:
            page_nr = 1
        elif page_nr > paginator.num_pages:
            page_nr = paginator.num_pages
    except ValueError:
        page_nr = 1
    page_obj = paginator.get_page(page_nr)
    page_range = paginator.get_elided_page_range(page_nr, on_each_side=2, on_ends=1)
    context = {
        'categories': categories,
        'page_obj': page_obj,
        'page_range': page_range,
        'category': category
    }
    return render(request, 'blog/category_view.html', context)


def subcategory_view(request, slug):
    categories = Category.objects.all()
    try:
        subcategory = Subcategory.objects.get(slug=slug)
    except Subcategory.DoesNotExist:
        subcategory = None
    posts = Post.objects.filter(published=True, subcategory__slug__exact=slug)
    paginator = Paginator(posts, 4)
    page_nr = request.GET.get('page', 1)
    try:
        page_nr = int(page_nr)
        if page_nr < 1:
            page_nr = 1
        elif page_nr > paginator.num_pages:
            page_nr = paginator.num_pages
    except ValueError:
        page_nr = 1
    page_obj = paginator.get_page(page_nr)
    page_range = paginator.get_elided_page_range(page_nr, on_each_side=2, on_ends=1)
    context = {
        'categories': categories,
        'page_obj': page_obj,
        'page_range': page_range,
        'subcategory': subcategory
    }
    return render(request, 'blog/subcategory_view.html', context)


def post_detail_view(request, slug):
    categories = Category.objects.all()
    post = get_object_or_404(Post, slug=slug)
    photos = post.photo.all()[1:]
    similar_posts = Post.objects.filter(subcategory=post.subcategory).exclude(pk=post.pk)
    similar_posts_len = len(similar_posts) if len(similar_posts) <= 4 else 4
    similar_posts = random.sample(list(similar_posts), k=similar_posts_len)
    try:
        previous_post = Post.objects.filter(created_on__lte=post.created_on).exclude(pk=post.pk)[0]
    except IndexError:
        previous_post = ''
    try:
        next_post = Post.objects.filter(created_on__gte=post.created_on).exclude(pk=post.pk).order_by('created_on')[0]
    except IndexError:
        next_post = ''
    comments = Comment.objects.filter(post=post, published=True, reply_to__exact=None).order_by('-created_on')
    comments_count = Comment.objects.filter(post=post, published=True).count()
    context = {
        'categories': categories,
        'post': post,
        'photos': photos,
        'more_posts': similar_posts,
        'previous_post': previous_post,
        'next_post': next_post,
        'comments': comments,
        'comments_count': comments_count
    }
    if request.method == 'POST':
        form = CommentForm(request.POST)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print('sama forma prawidłowa')
            try:
                reply_to_pk = int(form.cleaned_data['reply_to'])
                new_comment = Comment(
                    post=post,
                    reply_to=Comment.objects.get(pk=reply_to_pk),
                    name=form.cleaned_data['name'],
                    content=form.cleaned_data['content'],
                    email=form.cleaned_data['email']
                )
                new_comment.save()
            except (TypeError, ValueError, Comment.DoesNotExist):
                new_comment = Comment(
                    post=post,
                    name=form.cleaned_data['name'],
                    content=form.cleaned_data['content'],
                    email=form.cleaned_data['email']
                )
                new_comment.save()
            return redirect(reverse('blog:post_detail', kwargs={'slug': slug}))
    else:
        form = CommentForm()
    captcha1 = random.randint(11, 29)
    captcha2 = random.randint(1, 9)
    context['captcha1'] = captcha1
    context['captcha2'] = captcha2
    valid_captcha = captcha1 - captcha2
    context['valid_captcha'] = valid_captcha

    context['form'] = form

    return render(request, 'blog/post_detail_view.html', context)


def newsletter_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'bad_request': '',
        'subscriber': '',
        'error': ''
    }
    if request.method == 'GET':
        context['bad_request'] = 'Bad request attempt'
    else:
        email = request.POST.get('email', '')
        pattern = r'^([A-Za-z0-9]+[.-_]?)*[A-Za-z0-9]+@[A-Za-z]{2,20}(\.[A-Za-z]{2,3})+$'
        result = re.match(pattern, email)
        if result:
            try:
                NewsletterSubscriber.objects.get(email=email)
                context['subscriber'] = 'Email address already exists'
            except NewsletterSubscriber.DoesNotExist:
                new_subscriber = NewsletterSubscriber(email=email)
                new_subscriber.save()
                send_mail(
                    f'Thank you for subscribing {request.get_host()}',
                    f'Thank you for subscribing {request.get_host()}\n'
                    'From now you will receive notifications about new recipes on the website.',
                    'felidevsender@gmail.com',
                    [str(new_subscriber.email)]
                )
        else:
            context['error'] = 'Incorrect email address'
    return render(request, 'blog/newsletter_view.html', context)
