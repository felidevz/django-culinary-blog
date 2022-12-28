from django import forms
from django.core.exceptions import ValidationError

from .models import NewsletterSubscriber


class NewsletterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'email'}))

    def clean_email(self):
        cleaned_email = self.cleaned_data['email']
        if NewsletterSubscriber.objects.filter(email=cleaned_email).exists():
            raise ValidationError('Użytkownik o podanym adresie email już istnieje.')
        return cleaned_email


class CommentForm(forms.Form):
    reply_to = forms.CharField(widget=forms.HiddenInput, required=False)
    name = forms.CharField(label='Imię', max_length=50)
    content = forms.CharField(label='Komentarz', widget=forms.Textarea)
    email = forms.EmailField(label='Email')
    captcha = forms.CharField(label='Rozwiąż', widget=forms.NumberInput)
    valid_captcha = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, prefix='comment-add', auto_id=True)

    def clean_name(self):
        cleaned_name = self.cleaned_data['name']
        if not cleaned_name.isalpha():
            raise ValidationError('Pole powinno zawierać wyłącznie litery alfabetu.')
        return cleaned_name

    def clean(self):
        cleaned_data = super().clean()
        cleaned_captcha = cleaned_data['captcha']
        cleaned_valid_captcha = cleaned_data['valid_captcha']
        if not cleaned_captcha == cleaned_valid_captcha:
            self.add_error('captcha', ValidationError('Niepoprawny wynik CAPTCHA. Spróbuj jeszcze raz.'))
        return cleaned_data
