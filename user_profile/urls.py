from django.urls import path
from django.views.generic import TemplateView
from .views import PaymentHistoryView,ExtractionHistoryView,download,ProfileView

app_name = 'user_profile'
urlpatterns = [
    path('account_settings/', ProfileView,
         name="account_settings"),
    path('extraction_history/', ExtractionHistoryView, name="extraction_history"),
    path('payment_history/', PaymentHistoryView, name="payment_history"),
    path('download/<path:path>/', download, name="download"),

]
