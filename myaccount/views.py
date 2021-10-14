from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib import messages
from twitter_data_extractor.settings.prod import EMAIL_HOST_USER

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .models import CustomUser,Profile
from .tokens import account_activation_token

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('scraper:dashboard'))
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('myaccount:login')
    else:
        form = LoginForm()
    return render(request, 'myaccount/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            # login(request, user)
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template()
            # and calls its render() method immediately.
            message = render_to_string('myaccount/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect(reverse('myaccount:activation_sent'))
            # return HttpResponseRedirect(reverse('scraper:dashboard'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'myaccount/signup.html', {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home:index'))


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        profile =Profile.objects.get(user=user)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        CustomUser.objects.filter(username=user.username).update(is_active=True)
        subject, from_email, to = 'Account confirmation', EMAIL_HOST_USER, EMAIL_HOST_USER
        html_content = render_to_string('myaccount/confirm_email.html', {'user':user})  # render with dynamic value
        text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse('scraper:dashboard'))
    else:
        return render(request, 'myaccount/activation_invalid.html')


def activation_sent_view(request):
    return render(request, 'myaccount/activation_sent.html')