from .models import Category


def categories(request):
    objects = Category.objects.all()
    return {'categories': objects}
