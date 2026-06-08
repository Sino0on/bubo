import requests
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Order
from .forms import OrderForm


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
        pass


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:success')

    def form_valid(self, form):
        order = form.save()
        send_telegram_notification(order)
        messages.success(self.request, 'Ваш заказ принят! Мы свяжемся с вами в ближайшее время.')
        return redirect(self.success_url)
