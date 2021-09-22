from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Job
from .forms import JobForm
from myaccount.models import Profile
from scraper.tasks import data_extract

@login_required
def dashboard(request):
    """ Twitter data extraction form"""
    current_user = request.user
    credit = current_user.profile.user_credit
    limit =int(current_user.profile.job_limit ) - int(current_user.profile.job_count )
    plan =  current_user.profile.plan
    if request.method == 'POST':

        # current_user = request.user
        # credit= current_user.profile.user_credit
        form = JobForm(request.POST)  # Display input form
        if form.is_valid():

            data = form.save(commit=False)  # save without commit
            if (request.user.profile.plan == "fr") & (data.limit>1000 ):
                return render(request,'scraper/tweet_limit.html')
            else:
                data.credits_required=current_user.profile.user_credit
                data.user = current_user
                data.save()  # save as a new job
                job = Job.objects.get(pk=data.id)  # get job id
                profile =Profile.objects.get(user=current_user)
                profile.job_count+=1
                new_limit = int(profile.job_limit - profile.job_count)
                if new_limit==0:
                    profile.user_credit=0
                    profile.plan="nn"
                    profile.job_limit=0
                    profile.job_count=0
                profile.save()
                data_extract.delay(job.id,current_user.id)  # function to extract the data
                #  celery worker -A twitter_data_extractor --loglevel=info
                # redis-server
                #./ngrok http 8000
                return redirect(reverse('scraper:thankyou'))
    else:
        form = JobForm()
    return render(request, 'scraper/index.html', {'form': form,'credit':credit,'limit':limit,'plan':plan})

