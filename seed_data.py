"""
Seed initial demo data.
Run: python seed_data.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bubostore.settings')
django.setup()

from catalog.models import Collection, Color, Product
from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@bubostore.kg', 'admin123')
    print('✓ Superuser: admin / admin123')

# Collections
play, _ = Collection.objects.get_or_create(
    slug='bubo-play',
    defaults={'name': 'Bubo Play', 'description': 'Игрушки и фигурки для детей и взрослых'}
)
nest, _ = Collection.objects.get_or_create(
    slug='bubo-nest',
    defaults={'name': 'Bubo Nest', 'description': 'Декор и полезные вещи для дома'}
)
print('✓ Collections created')

# Colors
colors_data = [
    ('Белый', '#FFFFFF'), ('Чёрный', '#1A1A1A'), ('Красный', '#E63946'),
    ('Синий', '#457B9D'), ('Зелёный', '#2D6A4F'), ('Жёлтый', '#F4D03F'),
    ('Оранжевый', '#E6A04A'), ('Бирюзовый', '#2C8C84'), ('Розовый', '#F48FB1'),
    ('Серый', '#9E9E9E'), ('Коричневый', '#795548'), ('Фиолетовый', '#7B1FA2'),
]
colors = {}
for name, hex_val in colors_data:
    c, _ = Color.objects.get_or_create(name=name, defaults={'hex': hex_val})
    colors[name] = c
print('✓ Colors created')

# Products
products_data = [
    {
        'name': 'Совёнок Bubo мини', 'slug': 'sovyonok-bubo-mini',
        'collection': play, 'price': 590,
        'description': 'Маленькая фигурка нашего маскота — мудрого филина Bubo. Отличный подарок и украшение для стола.',
        'material': 'PLA-пластик', 'size': '6×5×4 см', 'weight': '45 г', 'print_time': '2 часа',
        'is_hit': True, 'is_new': False,
        'colors': ['Белый', 'Оранжевый', 'Бирюзовый', 'Серый'],
    },
    {
        'name': 'Совёнок Bubo большой', 'slug': 'sovyonok-bubo-bolshoy',
        'collection': play, 'price': 990,
        'description': 'Большая фигурка Bubo — настоящий хранитель дома. Детали отличной чёткости, глаза выразительные.',
        'material': 'PLA-пластик', 'size': '12×9×7 см', 'weight': '110 г', 'print_time': '4 часа',
        'is_hit': True, 'is_new': True,
        'colors': ['Белый', 'Чёрный', 'Оранжевый', 'Бирюзовый', 'Серый', 'Фиолетовый'],
    },
    {
        'name': 'Динозавр Рекс', 'slug': 'dinozavr-reks',
        'collection': play, 'price': 750,
        'description': 'Классический тираннозавр Рекс — детализированная фигурка для игры или коллекции.',
        'material': 'PLA-пластик', 'size': '14×6×9 см', 'weight': '95 г', 'print_time': '3.5 часа',
        'is_hit': False, 'is_new': True,
        'colors': ['Зелёный', 'Жёлтый', 'Красный', 'Синий'],
    },
    {
        'name': 'Набор артикулированный дракон', 'slug': 'articulirovannyy-drakon',
        'collection': play, 'price': 1490,
        'description': 'Печатается прямо с шарнирами — каждое звено двигается. Без сборки, сразу гибкий!',
        'material': 'PLA-пластик', 'size': '30×6×4 см', 'weight': '180 г', 'print_time': '7 часов',
        'is_hit': True, 'is_new': False,
        'colors': ['Красный', 'Синий', 'Зелёный', 'Фиолетовый', 'Оранжевый', 'Чёрный'],
    },
    {
        'name': 'Органайзер для стола', 'slug': 'organayzer-dlya-stola',
        'collection': nest, 'price': 890,
        'description': 'Удобный органайзер для ручек, карандашей и мелочей. Лаконичный дизайн вписывается в любой интерьер.',
        'material': 'PLA-пластик', 'size': '10×10×8 см', 'weight': '120 г', 'print_time': '4 часа',
        'is_hit': True, 'is_new': False,
        'colors': ['Белый', 'Чёрный', 'Серый', 'Бирюзовый'],
    },
    {
        'name': 'Ваза геометрическая', 'slug': 'vaza-geometricheskaya',
        'collection': nest, 'price': 1190,
        'description': 'Изящная ваза с геометрическим паттерном. Подходит для сухих цветов и декоративных веток.',
        'material': 'PLA-пластик', 'size': '8×8×16 см', 'weight': '145 г', 'print_time': '5 часов',
        'is_hit': False, 'is_new': True,
        'colors': ['Белый', 'Чёрный', 'Серый', 'Коричневый'],
    },
    {
        'name': 'Крючки для прихожей (3 шт)', 'slug': 'kryuchki-prikhozhaya',
        'collection': nest, 'price': 690,
        'description': 'Набор из трёх настенных крючков. Монтаж на саморезы. Выдерживают до 2 кг каждый.',
        'material': 'PETG-пластик', 'size': '5×3×4 см каждый', 'weight': '60 г (набор)', 'print_time': '3 часа',
        'is_hit': False, 'is_new': False,
        'colors': ['Белый', 'Чёрный', 'Серый', 'Бирюзовый', 'Коричневый'],
    },
    {
        'name': 'Подставка для телефона', 'slug': 'podstavka-dlya-telefona',
        'collection': nest, 'price': 490,
        'description': 'Удобная подставка под любой смартфон. Подходит и для зарядки.',
        'material': 'PLA-пластик', 'size': '10×6×6 см', 'weight': '65 г', 'print_time': '2 часа',
        'is_hit': True, 'is_new': False,
        'colors': ['Белый', 'Чёрный', 'Серый', 'Оранжевый', 'Бирюзовый'],
    },
]

for data in products_data:
    color_names = data.pop('colors')
    if not Product.objects.filter(slug=data['slug']).exists():
        p = Product.objects.create(**data)
        p.colors.set([colors[n] for n in color_names if n in colors])
        print(f'  ✓ {p.name}')
    else:
        print(f'  — {data["name"]} already exists')

print('\n✅ Seed complete! Go to http://127.0.0.1:8000/admin  (admin / admin123)')
