"""Run: python manage.py shell < create_superuser.py"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bubostore.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@bubostore.kg', 'admin123')
    print('Superuser created: admin / admin123')
else:
    print('Superuser already exists')
