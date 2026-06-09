from django.contrib import admin
from django.utils.html import format_html
from .models import Collection, Color, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ('image', 'is_main', 'alt', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.image.url)
        return '—'
    preview.short_description = 'Превью'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Товаров'


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex', 'color_preview')
    search_fields = ('name',)

    def color_preview(self, obj):
        return format_html(
            '<div style="width:30px;height:30px;background:{};border-radius:50%;border:1px solid #ccc;"></div>',
            obj.hex
        )
    color_preview.short_description = 'Цвет'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'collection', 'price', 'in_stock',
        'is_hit', 'is_new', 'created_at', 'main_image_preview'
    )
    list_filter = ('collection', 'in_stock', 'is_hit', 'is_new')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('colors',)
    list_editable = ('in_stock', 'is_hit', 'is_new', 'price')
    inlines = [ProductImageInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'collection', 'description', 'price')
        }),
        ('Доступные цвета', {
            'fields': ('colors',),
        }),
        ('Характеристики', {
            'fields': ('material', 'size', 'weight', 'print_time'),
        }),
        ('Статус', {
            'fields': ('in_stock', 'is_hit', 'is_new'),
        }),
    )

    def main_image_preview(self, obj):
        img = obj.main_image()
        if img:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;" />', img.image.url)
        return '—'
    main_image_preview.short_description = 'Фото'
