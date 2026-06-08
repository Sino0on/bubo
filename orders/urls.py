from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'orders'

urlpatterns = [
    path('order/', views.OrderCreateView.as_view(), name='create'),
    path('order/success/', TemplateView.as_view(template_name='orders/success.html'), name='success'),
]
