from django.urls import path, include
from .views import dashboard
from django.views.generic import TemplateView

app_name = 'scraper'
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('thanks/',TemplateView.as_view(template_name="scraper/thankyou.html"),name ="thankyou"),

]
