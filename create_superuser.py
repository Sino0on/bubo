"""Run: python manage.py shell < create_superuser.py

Requires DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD
in the environment (see .env.example) — no hardcoded credentials.
"""
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bubostore.settings')
django.setup()

from django.contrib.auth import get_user_model

username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not username or not password:
    sys.exit('DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD must be set in the environment.')

User = get_user_model()
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email or '', password)
    print(f'Superuser created: {username}')
else:
    print('Superuser already exists')
