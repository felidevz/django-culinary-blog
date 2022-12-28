from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files import File
from django.db.models.query import QuerySet

from ..models import Category, Subcategory, Post, Photo, Comment


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User(username='testuser', is_staff=True, is_active=True)
        user.save()

        category = Category(name='Test category', slug='test-category')
        category.save()

        subcategory = Subcategory(category=category, name='Test subcategory', slug='test-subcategory')
        subcategory.save()

        cls.post = Post(
            created_by=user,
            title='Test post',
            slug='test-post',
            subcategory=subcategory,
            description='Test description',
            preparation='Test preparation'
        )
        cls.post.save()

        cls.post2 = Post(
            created_by=user,
            title='Test post 2',
            slug='test-post-2',
            subcategory=subcategory,
            description='Test description 2',
            preparation='Test preparation 2',
            published=False
        )
        cls.post2.save()

        cls.comment = Comment(
            post=cls.post,
            name='Test name',
            content='Test content',
            email='test@email.com',
            published=True
        )
        cls.comment.save()

        cls.comment2 = Comment(
            post=cls.post,
            name='Test name 2',
            content='Test content 2',
            email='test2@email.com',
        )
        cls.comment2.save()

    def test_str(self):
        self.assertEqual(str(self.post), 'Test post')

    def test_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/test-post/')

    def test_main_photo(self):
        # Test without photos
        self.assertEqual(self.post.get_main_photo(), '')

        # Test with photos
        photo1_opened = File(open(settings.BASE_DIR / 'blog' / 'tests' / 'test-photo1.jpg', 'rb'))
        photo1 = Photo(post=self.post)
        photo1.image.save('test-photo1.jpg', photo1_opened)

        photo2_opened = File(open(settings.BASE_DIR / 'blog' / 'tests' / 'test-photo2.jpg', 'rb'))
        photo2 = Photo(post=self.post)
        photo2.image.save('test-photo2.jpg', photo2_opened)

        photo3_opened = File(open(settings.BASE_DIR / 'blog' / 'tests' / 'test-photo3.jpg', 'rb'))
        photo3 = Photo(post=self.post)
        photo3.image.save('test-photo3.jpg', photo3_opened)

        self.assertEqual(self.post.get_main_photo(), photo1)

        photo1.image.delete()
        photo2.image.delete()
        photo3.image.delete()

    def test_secondary_photos(self):
        # Test without photos
        self.assertEqual(type(self.post.get_secondary_photos()), QuerySet)
        self.assertEqual(len(self.post.get_secondary_photos()), 0)

        # Test with photos
        photo1_opened = File(open(settings.BASE_DIR / 'blog' / 'tests' / 'test-photo1.jpg', 'rb'))
        photo1 = Photo(post=self.post)
        photo1.image.save('test-photo1.jpg', photo1_opened)

        photo2_opened = File(open(settings.BASE_DIR / 'blog' / 'tests' / 'test-photo2.jpg', 'rb'))
        photo2 = Photo(post=self.post)
        photo2.image.save('test-photo2.jpg', photo2_opened)

        photo3_opened = File(open(settings.BASE_DIR / 'blog' / 'tests' / 'test-photo3.jpg', 'rb'))
        photo3 = Photo(post=self.post)
        photo3.image.save('test-photo3.jpg', photo3_opened)

        self.assertEqual(len(self.post.get_secondary_photos()), 2)
        self.assertEqual(self.post.get_secondary_photos()[0], photo2)
        self.assertEqual(self.post.get_secondary_photos()[1], photo3)

        photo1.image.delete()
        photo2.image.delete()
        photo3.image.delete()

    def test_comments_count(self):
        self.assertEqual(self.post.get_comments_count(), 1)

    def test_published_posts(self):
        self.assertEqual(len(Post.published_posts.all()), 1)
