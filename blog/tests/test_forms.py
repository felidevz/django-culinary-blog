from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import NewsletterSubscriber, Comment
from ..forms import NewsletterForm, CommentForm


class NewsletterFormTest(TestCase):
    def setUp(self):
        self.form = NewsletterForm(data={'email': 'test@email.com'})

    def test_valid_email(self):
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.clean_email(), 'test@email.com')

    def test_already_taken_email(self):
        self.assertTrue(self.form.is_valid())

        subscriber = NewsletterSubscriber.objects.create(email='test@email.com')
        subscriber.save()

        self.assertRaises(ValidationError, self.form.clean_email)


class CommentFormTest(TestCase):
    def test_valid_name(self):
        form = CommentForm(
            data={
                'comment-add-reply_to': '',
                'comment-add-name': 'Testname',
                'comment-add-content': 'Test content',
                'comment-add-email': 'test@email.com',
                'comment-add-captcha': '1',
                'comment-add-valid_captcha': '1'
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean_name(), 'Testname')

    def test_invalid_name(self):
        form = CommentForm(
            data={
                'comment-add-reply_to': '',
                'comment-add-name': 'Bad name',
                'comment-add-content': 'Test content',
                'comment-add-email': 'test@email.com',
                'comment-add-captcha': '1',
                'comment-add-valid_captcha': '1'
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(form['name'].errors, ['Pole powinno zawierać wyłącznie litery alfabetu.'])

    def test_valid_captcha(self):
        form = CommentForm(
            data={
                'comment-add-reply_to': '',
                'comment-add-name': 'Testname',
                'comment-add-content': 'Test content',
                'comment-add-email': 'test@email.com',
                'comment-add-captcha': '1',
                'comment-add-valid_captcha': '1'
            }
        )

        self.assertTrue(form.is_valid())

    def test_invalid_captcha(self):
        form = CommentForm(
            data={
                'comment-add-reply_to': '',
                'comment-add-name': 'Testname',
                'comment-add-content': 'Test content',
                'comment-add-email': 'test@email.com',
                'comment-add-captcha': '1',
                'comment-add-valid_captcha': '2'
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(form['captcha'].errors, ['Niepoprawny wynik CAPTCHA. Spróbuj jeszcze raz.'])
