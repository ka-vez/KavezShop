from django.urls import path
from . import views

urlpatterns = [
    path('payment-success', views.payment_success, name='payment-success'),
    path('checkout',views.checkout,name='checkout'),
    path('billing-info',views.billing_info, name='billing-info'),
    path('process-order', views.process_order, name='process-order'),
    path('shipped-dash', views.shipped_dash, name='ship-dash'),
    path('not-shipped-dash', views.not_shipped_dash, name='not-ship-dash'),
    path('orders/<int:pk>', views.orders, name='orders'),
]

