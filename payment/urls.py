from django.urls import path
from .views import checkout,process_payment,payment_canceled,payment_done
from django.views.generic import TemplateView

app_name = "payment"
urlpatterns = [
    path('checkout/',checkout, name='checkout'),
    path('process-payment/<int:amount>', process_payment, name='process_payment'),
    path('payment-done/', payment_done, name='payment_done'),
    path('payment-cancelled/', payment_canceled, name='payment_cancelled'),


]
