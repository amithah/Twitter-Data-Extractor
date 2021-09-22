from django.urls import path
from .views import home,thankyou

app_name = 'home'
urlpatterns = [
    path('',home ,name='index'),
    path('thankyou/',thankyou,name='thankyou')


]
