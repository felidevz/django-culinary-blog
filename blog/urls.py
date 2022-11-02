from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('subcategory/<slug:slug>/', views.subcategory_view, name='subcategory'),
    path('newsletter/', views.newsletter_view, name='newsletter')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
