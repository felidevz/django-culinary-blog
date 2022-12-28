from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

from ..models import Category, Subcategory, Post, Comment
from ..forms import CommentForm


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.user = User(
            username='testuser',
            is_staff=True,
            is_active=True
        )
        self.user.save()

        category = Category(
            name='Test category',
            slug='test-category'
        )
        category.save()

        subcategory = Subcategory(
            category=category,
            name='Test subcategory',
            slug='test-subcategory'
        )
        subcategory.save()

        for i in range(7):
            post = Post.objects.create(
                created_by=self.user,
                title=f'Test post {i}',
                slug=f'test-post-{i}',
                subcategory=subcategory,
                description=f'Test description {i}',
                preparation=f'Test preparation {i}'
            )
            post.save()

        comment = Comment(
            post=Post.objects.get(pk=1),
            name='Test name',
            content='Test content',
            email='test@email.com',
            published=True
        )
        comment.save()

        comment2 = Comment(
            post=Post.objects.get(pk=1),
            name='Test name 2',
            content='Test content 2',
            email='test2@email.com',
            published=True
        )
        comment2.save()

    def test_url_exists(self):
        response = self.client.get('/post/test-post-0/')

        self.assertEqual(response.status_code, 200)

    def test_url_reverse(self):
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'test-post-0'}))

        self.assertEqual(response.status_code, 200)

    def test_used_template(self):
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'test-post-0'}))

        self.assertTemplateUsed(response, 'blog/post_detail_view.html')

    def test_template_content(self):
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'test-post-0'}))

        self.assertContains(response, '<title>Test post 0 |')
        self.assertContains(response, 'Test category')
        self.assertContains(response, 'test-category')
        self.assertContains(response, 'Test subcategory')
        self.assertContains(response, 'test-subcategory')

    def test_form_comment_add_without_reply_and_user(self):
        response = self.client.post(reverse('blog:post_detail', kwargs={'slug': 'test-post-0'}), data={
            'comment-add-name': 'Testname',
            'comment-add-content': 'Test content',
            'comment-add-email': 'valid@email.com',
            'comment-add-captcha': '1',
            'comment-add-valid_captcha': '1'
        })

        self.assertEqual(response.status_code, 302)
        comment = Comment.objects.get(name='Testname')
        self.assertEqual(comment.reply_to, None)
        self.assertFalse(comment.is_post_author)
        self.assertFalse(comment.published)

    def test_form_comment_add_with_reply_and_user(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('blog:post_detail', kwargs={'slug': 'test-post-0'}), data={
            'comment-add-reply_to': '2',
            'comment-add-name': 'Testname',
            'comment-add-content': 'Test content',
            'comment-add-email': 'valid@email.com',
            'comment-add-captcha': '1',
            'comment-add-valid_captcha': '1'
        })

        self.assertEqual(response.status_code, 302)
        comment = Comment.objects.get(name='Testname')
        self.assertEqual(comment.reply_to, Comment.objects.get(pk=2))
        self.assertTrue(comment.is_post_author)
        self.assertTrue(comment.published)

    def test_form_comment_add_with_invalid_reply(self):
        response = self.client.post(reverse('blog:post_detail', kwargs={'slug': 'test-post-0'}), data={
            'comment-add-reply_to': '5',
            'comment-add-name': 'Testname',
            'comment-add-content': 'Test content',
            'comment-add-email': 'valid@email.com',
            'comment-add-captcha': '1',
            'comment-add-valid_captcha': '1'
        })

        self.assertEqual(response.status_code, 302)
        comment = Comment.objects.get(name='Testname')
        self.assertEqual(comment.reply_to, None)
