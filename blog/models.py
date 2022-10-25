from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='post_created', null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='post_modified', null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    preparation_time = models.CharField(max_length=20)
    title = models.CharField(max_length=60)
    slug = models.SlugField(max_length=80, unique=True)
    subcategory = models.ForeignKey('Subcategory', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    preparation = models.TextField()
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)

    def __str__(self):
        return self.content


class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photo')
    image = models.ImageField(upload_to='blog/')

    def __str__(self):
        return self.image.name


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategory')
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
