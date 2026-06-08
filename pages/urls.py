from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.AboutView.as_view(), name='about'),
    path('delivery/', views.DeliveryView.as_view(), name='delivery'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
]
