from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from catalog.sitemaps import StaticSitemap, CollectionSitemap, ProductSitemap
from catalog.views import HomeView

sitemaps = {
    'static':      StaticSitemap,
    'collections': CollectionSitemap,
    'products':    ProductSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('catalog/', include('catalog.urls')),
    path('', include('pages.urls')),
    path('', include('orders.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'bubostore.views.handler404'
handler500 = 'bubostore.views.handler500'
