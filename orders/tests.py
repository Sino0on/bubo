from django.test import TestCase
from django.urls import reverse

from catalog.models import Collection, Color, Product

from .models import Order


class OrderCreateViewTests(TestCase):
    def setUp(self):
        collection = Collection.objects.create(name='Bubo Play', slug='bubo-play')
        self.color = Color.objects.create(name='Белый', hex='#FFFFFF')
        self.product = Product.objects.create(
            name='Совёнок Bubo мини',
            slug='sovyonok-bubo-mini',
            collection=collection,
            description='Тестовое описание',
            price=590,
        )

    def _valid_payload(self, **overrides):
        payload = {
            'name': 'Иван',
            'phone': '+996700000000',
            'product': self.product.pk,
            'color': self.color.pk,
            'quantity': 1,
            'delivery_method': 'pickup',
            'comment': '',
            'website': '',
        }
        payload.update(overrides)
        return payload

    def test_valid_order_is_created_and_redirects(self):
        response = self.client.post(reverse('orders:create'), self._valid_payload())
        self.assertRedirects(response, reverse('orders:success'))
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get()
        self.assertEqual(order.name, 'Иван')
        self.assertTrue(order.ip_address)

    def test_honeypot_filled_does_not_create_order(self):
        response = self.client.post(
            reverse('orders:create'),
            self._valid_payload(website='http://spam.example'),
        )
        self.assertRedirects(response, reverse('orders:success'))
        self.assertEqual(Order.objects.count(), 0)

    def test_rate_limit_blocks_rapid_resubmit_from_same_ip(self):
        first = self.client.post(reverse('orders:create'), self._valid_payload())
        self.assertEqual(first.status_code, 302)

        second = self.client.post(reverse('orders:create'), self._valid_payload(name='Пётр'))
        self.assertEqual(second.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
