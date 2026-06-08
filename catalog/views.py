from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from .models import Product, Collection, Color


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['hits'] = Product.objects.filter(is_hit=True, in_stock=True).prefetch_related('images')[:6]
        ctx['news'] = Product.objects.filter(is_new=True, in_stock=True).prefetch_related('images')[:6]
        ctx['collections'] = Collection.objects.all()
        return ctx


class CatalogListView(ListView):
    model = Product
    template_name = 'catalog/list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.prefetch_related('images', 'colors').select_related('collection')

        collection_slug = self.request.GET.get('collection')
        if collection_slug:
            qs = qs.filter(collection__slug=collection_slug)

        color_id = self.request.GET.get('color')
        if color_id:
            qs = qs.filter(colors__id=color_id)

        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        if price_min:
            qs = qs.filter(price__gte=price_min)
        if price_max:
            qs = qs.filter(price__lte=price_max)

        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

        sort = self.request.GET.get('sort', '-created_at')
        if sort in ('-created_at', 'created_at', 'price', '-price'):
            qs = qs.order_by(sort)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['collections'] = Collection.objects.all()
        ctx['colors'] = Color.objects.all()
        ctx['current_params'] = self.request.GET.copy()
        return ctx


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/detail.html'
    context_object_name = 'product'
    slug_field = 'slug'

    def get_queryset(self):
        return Product.objects.prefetch_related('images', 'colors').select_related('collection')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        product = self.object
        ctx['related'] = (
            Product.objects
            .filter(collection=product.collection)
            .exclude(pk=product.pk)
            .prefetch_related('images')[:4]
        )
        from django.conf import settings
        ctx['telegram_username'] = settings.TELEGRAM_USERNAME
        ctx['whatsapp_phone'] = settings.WHATSAPP_PHONE
        return ctx
