import logging
from datetime import timedelta

import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView

from .forms import OrderForm
from .models import Order

logger = logging.getLogger(__name__)

RATE_LIMIT_SECONDS = 60


def get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def send_telegram_notification(order):
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return
    text = (
        f"📦 Новый заказ #{order.pk}\n"
        f"👤 {order.name} | 📞 {order.phone}\n"
        f"🛍 {order.product.name}"
        f"{' | ' + order.color.name if order.color else ''}\n"
        f"📦 Кол-во: {order.quantity}\n"
        f"🚚 {order.get_delivery_method_display()}\n"
        f"💬 {order.comment or '—'}"
    )
    try:
        requests.post(
            f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage',
            data={'chat_id': settings.TELEGRAM_CHAT_ID, 'text': text},
            timeout=5
        )
    except Exception:
        logger.exception('Failed to send Telegram notification for order #%s', order.pk)


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:success')

    def form_valid(self, form):
        if form.is_honeypot_filled():
            logger.warning('Order form honeypot triggered from IP %s', get_client_ip(self.request))
            return redirect(self.success_url)

        ip_address = get_client_ip(self.request)
        if ip_address:
            recent_cutoff = timezone.now() - timedelta(seconds=RATE_LIMIT_SECONDS)
            if Order.objects.filter(ip_address=ip_address, created_at__gte=recent_cutoff).exists():
                form.add_error(None, 'Вы уже отправили заказ недавно. Пожалуйста, подождите немного и попробуйте снова.')
                return self.form_invalid(form)

        order = form.save(commit=False)
        order.ip_address = ip_address
        order.save()
        send_telegram_notification(order)
        messages.success(self.request, 'Ваш заказ принят! Мы свяжемся с вами в ближайшее время.')
        return redirect(self.success_url)
