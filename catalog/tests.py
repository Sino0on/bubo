from django.test import TestCase
from django.urls import reverse

from .models import Collection, Color, Product


class CatalogViewsTests(TestCase):
    def setUp(self):
        self.collection = Collection.objects.create(name='Bubo Play', slug='bubo-play')
        self.color = Color.objects.create(name='Белый', hex='#FFFFFF')
        self.product = Product.objects.create(
            name='Совёнок Bubo мини',
            slug='sovyonok-bubo-mini',
            collection=self.collection,
            description='Тестовое описание',
            price=590,
        )
        self.product.colors.add(self.color)

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_catalog_list_loads(self):
        response = self.client.get(reverse('catalog:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_catalog_list_filters_do_not_error(self):
        params = {
            'collection': self.collection.slug,
            'color': self.color.id,
            'price_min': 100,
            'price_max': 1000,
            'q': 'Bubo',
            'sort': 'price',
        }
        response = self.client.get(reverse('catalog:list'), params)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_loads(self):
        response = self.client.get(reverse('catalog:detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_404_for_missing_slug(self):
        response = self.client.get(reverse('catalog:detail', kwargs={'slug': 'does-not-exist'}))
        self.assertEqual(response.status_code, 404)
