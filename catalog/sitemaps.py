from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, Collection


class StaticSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    pages = [
        ('home',           1.0),
        ('catalog:list',   0.9),
        ('pages:about',    0.5),
        ('pages:delivery', 0.5),
        ('pages:contacts', 0.5),
    ]

    def items(self):
        return self.pages

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return 'monthly' if item[1] < 0.9 else 'weekly'


class CollectionSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Collection.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Product.objects.filter(in_stock=True).order_by('-created_at')

    def lastmod(self, obj):
        return obj.created_at
