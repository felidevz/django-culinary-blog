from django.contrib import admin
from django.core.mail import send_mass_mail

from blog.models import Post, Ingredient, Photo, Category, Subcategory, NewsletterSubscriber, Comment


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    max_num = 3


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'subcategory', 'created_on', 'created_by', 'last_modified', 'modified_by', 'published')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [IngredientInline, PhotoInline]
    exclude = ('created_by', 'modified_by')

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            if obj.published:
                subscribers = NewsletterSubscriber.objects.all()
                message = (
                    f'{obj.title} - new recipe on {request.get_host()}',
                    f'New recipe available on {request.get_host()}\n'
                    f'Link: https://127.0.0.1:8000/{obj.slug}/',
                    'felidevsender@gmail.com',
                    [str(subscriber.email) for subscriber in subscribers if subscriber.email]
                )
                send_mass_mail((message,))
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    ordering = ('category',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(NewsletterSubscriber)
class NewsletterSubcriberAdmin(admin.ModelAdmin):
    list_display = ('email',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'created_on', 'published')
