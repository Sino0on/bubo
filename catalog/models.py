from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Collection(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Описание', blank=True)
    cover = models.ImageField('Обложка', upload_to='collections/', blank=True, null=True)

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:list') + f'?collection={self.slug}'


class Color(models.Model):
    name = models.CharField('Название цвета', max_length=50)
    hex = models.CharField('HEX-код', max_length=7, help_text='Например: #FF5733')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.hex})'


class Product(models.Model):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Slug', unique=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Коллекция', related_name='products'
    )
    description = models.TextField('Описание')
    price = models.DecimalField('Цена (сом)', max_digits=10, decimal_places=2)
    material = models.CharField('Материал', max_length=100, blank=True)
    size = models.CharField('Размер', max_length=100, blank=True, help_text='Например: 10×8×5 см')
    weight = models.CharField('Вес', max_length=50, blank=True, help_text='Например: 120 г')
    print_time = models.CharField('Время печати', max_length=50, blank=True, help_text='Например: 4 часа')
    colors = models.ManyToManyField(Color, verbose_name='Доступные цвета', blank=True)
    is_hit = models.BooleanField('Хит продаж', default=False)
    is_new = models.BooleanField('Новинка', default=False)
    in_stock = models.BooleanField('В наличии', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:detail', kwargs={'slug': self.slug})

    def main_image(self):
        img = self.images.filter(is_main=True).first()
        if not img:
            img = self.images.first()
        return img


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='images', verbose_name='Товар'
    )
    image = models.ImageField('Фото', upload_to='products/')
    is_main = models.BooleanField('Главное фото', default=False)
    alt = models.CharField('Alt-текст', max_length=200, blank=True)

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'
        ordering = ['-is_main', 'id']

    def __str__(self):
        return f'Фото {self.product.name}'
