from django.conf import settings
from .models import Collection


def collections_processor(request):
    return {
        'all_collections': Collection.objects.all(),
        'SITE_URL':        getattr(settings, 'SITE_URL', ''),
        'SITE_NAME':       getattr(settings, 'SITE_NAME', 'Bubo 3D Store'),
        'YANDEX_METRIKA_ID': getattr(settings, 'YANDEX_METRIKA_ID', ''),
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', ''),
    }
