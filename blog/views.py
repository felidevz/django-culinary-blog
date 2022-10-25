from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import Http404
from django.core.mail import send_mail

from blog.models import Post, Ingredient, Photo, Category, Subcategory, NewsletterSubscriber
import re


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
