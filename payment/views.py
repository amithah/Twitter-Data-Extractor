from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from .models import Payment


def checkout(request):
    #
    # request.session['amount'] == amount
    return redirect(reverse('payment:process_payment'))


def process_payment(request,amount):
    payment= Payment()
    payment.user = request.user
    payment.save()
    # job_id = request.session.get('job_id')
    # payment_id = request.session.get('payment_id')
    payment_id = payment.id
    user = request.user
    # job = get_object_or_404(Job, id=job_id)
    host = request.get_host()
    amount=amount
    # if user.profile.plan =="ot":
    #     amount = 10
    # elif user.profile.plan =="mn":
    #     amount = 30
    # else:
    #     amount=100
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': f"{amount}",
        'item_name': f"{user.username}_{payment_id}",
        'invoice': f"{user.id}_{payment_id}_{amount}",
        'custom': f"{payment_id}",
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment:payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment:payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process_payment.html', {'form': form})


@csrf_exempt
def payment_done(request):
    return render(request, 'payment/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/payment_cancelled.html')
