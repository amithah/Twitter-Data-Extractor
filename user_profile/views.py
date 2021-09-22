from django.shortcuts import render, redirect, reverse
from payment.models import Payment
from scraper.models import Job
from django.http import HttpResponse

import os
from django.conf import settings
from django.http import HttpResponse, Http404

from django.template import loader

def ProfileView(request):
    current_user = request.user
    credit = current_user.profile.user_credit
    limit = int(current_user.profile.job_limit) - int(current_user.profile.job_count)
    return render(request, "user_profile/account_settings.html", {'limit':limit,})

def PaymentHistoryView(request):
    user = request.user
    payment_list =[]
    payment_list = Payment.objects.filter(user=user)
    return render(request, "user_profile/payment_history.html", {'payment_list': payment_list})


def ExtractionHistoryView(request):
    user = request.user
    job_list =[]
    job_list = Job.objects.filter(user=user)
    return render(request, "user_profile/extraction_history.html", {'job_list':job_list})



def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/csv")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404