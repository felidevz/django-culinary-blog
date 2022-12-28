from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published=True)


class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='post_created', null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='post_modified', null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    title = models.CharField(max_length=60)
    slug = models.SlugField(max_length=80, unique=True)
    subcategory = models.ForeignKey('Subcategory', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    preparation = models.TextField()
    source = models.CharField(max_length=120, null=True, blank=True)
    published = models.BooleanField(default=True)
    objects = models.Manager()
    published_posts = PublishedPostManager()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def get_main_photo(self):
        try:
            main_photo = self.photos.all()[0]
        except IndexError:
            main_photo = ''
        return main_photo

    def get_secondary_photos(self):
        secondary_photos = self.photos.all()[1:]
        return secondary_photos

    def get_comments_count(self):
        comments = Comment.published_comments.filter(post=self)
        return comments.count()


class Ingredient(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ingredients')
    content = models.CharField(max_length=100)

    def __str__(self):
        return self.content


class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='blog/')

    def __str__(self):
        return self.image.url


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return self.category.name + ' -> ' + self.name

    def get_absolute_url(self):
        return reverse('blog:subcategory', kwargs={'slug': self.slug})


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class PublishedCommentsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    reply_to = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='reply_comments', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    content = models.TextField()
    email = models.EmailField()
    published = models.BooleanField(default=False)
    is_post_author = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='blog/', default='blog/anonymous-user.png')
    objects = models.Manager()
    published_comments = PublishedCommentsManager()

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.content
