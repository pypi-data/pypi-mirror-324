from django.urls import path
from . import views

app_name = 'django_intram'

urlpatterns = [
    path('payment/init/', views.initialize_payment, name='initialize_payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('payment/status/<str:transaction_id>/', views.payment_status, name='payment_status'),
]
