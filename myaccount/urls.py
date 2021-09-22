from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import signup_view,activate,activation_sent_view
from . import views
from django.urls import reverse_lazy

app_name = 'myaccount'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', signup_view, name="signup"),
    # reset password urls
    path('password_reset/', auth_views. PasswordResetView.as_view(
        template_name='myaccount/password_reset_form.html',
        subject_template_name='myaccount/password_reset_subject.txt',
        email_template_name = 'myaccount/password_reset_email.html',
        success_url = reverse_lazy('myaccount:password_reset_done')),
        name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='myaccount/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='myaccount/password_reset_confirm.html',
         success_url=reverse_lazy('myaccount:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='myaccount/password_reset_complete.html'),
         name='password_reset_complete'),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),


]
