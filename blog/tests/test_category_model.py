from django.test import TestCase

from ..models import Category


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category(name='Test category', slug='test-category')
        cls.category.save()

    def test_str(self):
        self.assertEqual(str(self.category), 'Test category')

    def test_absolute_url(self):
        self.assertEqual(self.category.get_absolute_url(), '/category/test-category/')
