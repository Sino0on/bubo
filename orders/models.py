from django.db import models
from catalog.models import Product, Color


class Order(models.Model):
    DELIVERY_CHOICES = [
        ('pickup', 'Самовывоз (Бишкек)'),
        ('delivery', 'Доставка по городу'),
        ('mail', 'Доставка по Кыргызстану'),
    ]
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтверждён'),
        ('printing', 'В печати'),
        ('ready', 'Готов'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True,
        verbose_name='Товар', related_name='orders'
    )
    color = models.ForeignKey(
        Color, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Выбранный цвет'
    )
    quantity = models.PositiveSmallIntegerField('Количество', default=1)
    delivery_method = models.CharField(
        'Способ получения', max_length=20,
        choices=DELIVERY_CHOICES, default='pickup'
    )
    comment = models.TextField('Комментарий', blank=True)
    status = models.CharField(
        'Статус', max_length=20,
        choices=STATUS_CHOICES, default='new'
    )
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.pk} — {self.name} ({self.product})'
