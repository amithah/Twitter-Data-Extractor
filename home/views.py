from django.core.mail import send_mail
from django.shortcuts import render,redirect,reverse
from .forms import ContactForm

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from twitter_data_extractor.settings.prod import DEFAULT_FROM_EMAIL,EMAIL_HOST_USER


def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            to= EMAIL_HOST_USER
            subject, from_email= 'Contact form message', DEFAULT_FROM_EMAIL

            html_content = render_to_string('home/email.html', {'contact': contact})  # render with dynamic value
            text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

            # create the email, and attach the HTML version as well.
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)

        return redirect(reverse('home:thankyou'))
    else:
        form = ContactForm()
    return render(request, 'home/index.html', {'form': form})

def thankyou(request):
    return render(request, "home/thankyou.html")