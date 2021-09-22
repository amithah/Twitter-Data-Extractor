from django.shortcuts import get_object_or_404
from payment.models import Payment
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from myaccount.models import Profile
from scraper.models import Job


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    print(ipn.payment_status)
    if ipn.payment_status == 'Completed':
        # payment was successful
        payment = get_object_or_404(Payment, id=int(ipn.custom))
        payment.status = True
        payment.credits_added = ipn.mc_gross
        payment.save()
        profile = get_object_or_404(Profile, user=payment.user)

        limit=int((profile.job_limit)-(profile.job_count))
        profile.user_credit = ipn.mc_gross

        if ipn.mc_gross == 10:
            profile.plan = "ot"
            profile.job_limit = limit +1
        elif ipn.mc_gross == 30:
            profile.plan = "mn"
            profile.job_limit = limit + 30
        else:
            profile.plan = "yr"
            profile.job_limit = limit + 100
        profile.job_count = 0
        profile.save()
        # user = Job.objects.get(user=job.user)
        # data_extract.delay(job.id, user.id)  # function to extract the data
